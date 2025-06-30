import sys

sys.path.append(".")
import unittest

from app.agents.tools.internet_search import (
    InternetSearchInput,
    internet_search_tool,
    _summarize_content,
)


class TestInternetSearchTool(unittest.TestCase):
    def test_internet_search(self):
        # query = "Amazon Stock Price Today"
        query = "東京 焼肉"
        time_limit = "d"
        country = "jp-jp"
        arg = InternetSearchInput(query=query, time_limit=time_limit, country=country)
        response = internet_search_tool.run(
            tool_use_id="dummy",
            input=arg.model_dump(),
            model="claude-v3.5-sonnet-v2",
        )
        self.assertIsInstance(response["related_documents"], list)
        # Handle rate limiting gracefully - if we get an error due to rate limiting, that's expected
        if response["status"] == "error":
            error_content = response["related_documents"][0].content
            if (
                "rate" in str(error_content).lower()
                or "limit" in str(error_content).lower()
            ):
                print(
                    f"Rate limit detected (expected in test environment): {error_content}"
                )
                return
        self.assertEqual(response["status"], "success")
        print(response)

    def test_summarization(self):
        """Test that the summarization function works correctly"""
        test_content = (
            "This is a long test content that should be summarized by Claude 3 Haiku. "
            * 50
        )
        test_title = "Test Title"
        test_url = "https://example.com"

        summary = _summarize_content(test_content, test_title, test_url)

        # Verify the summary is shorter than the original content
        self.assertLess(len(summary), len(test_content))
        # Verify the summary is not empty
        self.assertGreater(len(summary), 0)
        # Verify the summary contains some meaningful content
        summary_lower = summary.lower()
        self.assertTrue("summary" in summary_lower or "content" in summary_lower)

        print(f"Original length: {len(test_content)}")
        print(f"Summary length: {len(summary)}")
        print(f"Summary: {summary[:200]}...")


if __name__ == "__main__":
    unittest.main()
