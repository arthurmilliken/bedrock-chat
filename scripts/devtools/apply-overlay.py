#!/usr/bin/env python3
"""
Overlay Applicator - Environment-specific Configuration Management

This script applies environment-specific overlays to a base project configuration.
It supports file replacement, JSON merging, and patch application strategies.

Usage:
    python scripts/devtools/apply-overlay.py [overlay_name]

Examples:
    python scripts/devtools/apply-overlay.py default
    python scripts/devtools/apply-overlay.py production
    python scripts/devtools/apply-overlay.py development

Directory Structure:
    overlays/
    ├── default/
    │   ├── overlay.config.json     # Configuration manifest
    │   ├── cdk/
    │   │   └── parameter.ts        # Direct replacement files
    │   ├── configs/
    │   │   └── cdk.json           # Files for JSON merge operations
    │   └── patches/
    │       ├── package.json.patch  # Unix patch files
    │       └── package.json.json   # JSON replacement rules
    └── production/
        ├── overlay.config.json
        └── ...

Configuration Format (overlay.config.json):
    {
      "metadata": {
        "name": "default",
        "description": "default environment overlay",
        "version": "1.0.0"
      },
      "files": {
        "cdk/parameter.ts": "cdk/parameter.ts",     # Direct replacement
        "cdk.json": "merge",                        # Smart JSON merge
        "package.json": "patch"                     # Apply patch
      }
    }

Application Strategies:
    1. Direct Replacement: Copy overlay file to target location
    2. Smart Merge: Deep merge JSON configurations
    3. Patch Application: Apply Unix patches or string replacements
"""

import json
import shutil
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class OverlayApplicator:
    """
    Applies environment-specific configuration overlays to a project.

    This class manages the application of overlay files using different strategies:
    - File replacement for complete configuration overwrites
    - JSON merging for partial configuration updates
    - Patch application for surgical modifications

    Attributes:
        overlay_path (Path): Path to the overlay directory
        config (Dict[str, Any]): Loaded overlay configuration
        backup_dir (Optional[Path]): Directory for backup files
    """

    def __init__(self, overlay_name: str = "default", create_backups: bool = False):
        """
        Initialize the overlay applicator.

        Args:
            overlay_name (str): Name of the overlay to apply
            create_backups (bool): Whether to create backup files before modification

        Raises:
            FileNotFoundError: If overlay directory or config file doesn't exist
            json.JSONDecodeError: If overlay.config.json is malformed
        """
        self.overlay_path = Path(f"overlays/{overlay_name}")
        self.backup_dir = Path(f".backups/{overlay_name}") if create_backups else None

        if not self.overlay_path.exists():
            raise FileNotFoundError(f"Overlay directory not found: {self.overlay_path}")

        config_path = self.overlay_path / "overlay.config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_path}: {e}")

        # Validate required configuration structure
        if "files" not in self.config:
            raise ValueError("overlay.config.json must contain a 'files' section")

        if self.backup_dir:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

    def apply(self) -> None:
        """
        Apply all overlay configurations defined in overlay.config.json.

        Processes each file entry in the configuration and applies the appropriate
        transformation strategy (replace, merge, or patch).

        Raises:
            Exception: If any file processing fails
        """
        print(f"🚀 Applying overlay: {self.overlay_path.name}")

        if "metadata" in self.config:
            metadata = self.config["metadata"]
            print(f"   Description: {metadata.get('description', 'No description')}")
            print(f"   Version: {metadata.get('version', 'Unknown')}")

        try:
            processed_files = []

            for target_file, source in self.config["files"].items():
                print(f"   Processing: {target_file} ← {source}")
                self._process_file(target_file, source)
                processed_files.append(target_file)

            print(f"✅ Overlay applied successfully!")
            print(f"   Modified {len(processed_files)} file(s)")

            if self.backup_dir:
                print(f"   Backups stored in: {self.backup_dir}")

        except Exception as e:
            print(f"❌ Overlay application failed: {e}")
            print(f"   Error occurred while processing overlay files")
            raise

    def _process_file(self, target_file: str, source: str) -> None:
        """
        Process a single file based on the specified strategy.

        Args:
            target_file (str): Path to the target file to modify
            source (str): Source strategy or file path

        Raises:
            FileNotFoundError: If source file doesn't exist for replacement
            Exception: If processing fails
        """
        target_path = Path(target_file)

        # Create backup if requested
        if self.backup_dir and target_path.exists():
            backup_path = self.backup_dir / target_file.replace("/", "_")
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_path, backup_path)

        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if source == "merge":
            self._smart_merge(target_path)
        elif source == "patch":
            self._apply_patch(target_path)
        else:
            # Direct replacement
            self._direct_replacement(target_path, source)

    def _direct_replacement(self, target_path: Path, source: str) -> None:
        """
        Perform direct file replacement.

        Args:
            target_path (Path): Target file to replace
            source (str): Relative path to source file within overlay

        Raises:
            FileNotFoundError: If source file doesn't exist
        """
        source_path = self.overlay_path / source

        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        shutil.copy2(source_path, target_path)
        print(f"     → Replaced with {source_path}")

    def _smart_merge(self, target_path: Path) -> None:
        """
        Perform intelligent JSON merging.

        Deep merges the overlay JSON with the existing target file,
        preserving the base structure while applying overlay changes.

        Args:
            target_path (Path): Target JSON file to merge

        Raises:
            FileNotFoundError: If overlay config file doesn't exist
            json.JSONDecodeError: If JSON files are malformed
        """
        overlay_file = self.overlay_path / "configs" / target_path.name

        if not overlay_file.exists():
            raise FileNotFoundError(f"Overlay config not found: {overlay_file}")

        # Load both configurations
        base_config = {}
        if target_path.exists():
            with open(target_path, "r", encoding="utf-8") as f:
                base_config = json.load(f)

        with open(overlay_file, "r", encoding="utf-8") as f:
            overlay_config = json.load(f)

        # Perform deep merge
        merged = self._deep_merge(base_config, overlay_config)

        # Write merged configuration
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)

        print(f"     → Merged with {overlay_file}")

    def _deep_merge(
        self, base: Dict[str, Any], overlay: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recursively merge two dictionaries.

        Args:
            base (Dict[str, Any]): Base configuration
            overlay (Dict[str, Any]): Overlay configuration

        Returns:
            Dict[str, Any]: Merged configuration
        """
        result = base.copy()

        for key, value in overlay.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def _apply_patch(self, target_path: Path) -> None:
        """
        Apply patches to modify existing file content.

        Supports two patch formats:
        1. Unix patch files (.patch) - Applied using system patch command
        2. JSON replacement files (.json) - Simple string replacements

        Args:
            target_path (Path): Target file to patch

        Raises:
            Exception: If patch application fails
        """
        patch_file = self.overlay_path / "patches" / f"{target_path.name}.patch"
        replacements_file = self.overlay_path / "patches" / f"{target_path.name}.json"

        if patch_file.exists():
            self._apply_unix_patch(target_path, patch_file)
        elif replacements_file.exists():
            self._apply_string_replacements(target_path, replacements_file)
        else:
            raise FileNotFoundError(
                f"No patch file found for {target_path.name} "
                f"(looked for {patch_file} or {replacements_file})"
            )

    def _apply_unix_patch(self, target_path: Path, patch_file: Path) -> None:
        """Apply Unix patch file using system patch command."""
        result = subprocess.run(
            ["patch", str(target_path), str(patch_file)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(f"Unix patch failed: {result.stderr}")

        print(f"     → Applied Unix patch {patch_file}")

    def _apply_string_replacements(
        self, target_path: Path, replacements_file: Path
    ) -> None:
        """Apply string replacements from JSON file."""
        with open(replacements_file, "r", encoding="utf-8") as f:
            replacements = json.load(f)

        if not target_path.exists():
            raise FileNotFoundError(
                f"Target file not found for patching: {target_path}"
            )

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        for old, new in replacements.items():
            content = content.replace(old, new)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"     → Applied {len(replacements)} string replacement(s)")

    def list_files(self) -> None:
        """List all files that would be affected by this overlay."""
        print(f"📋 Files managed by overlay '{self.overlay_path.name}':")

        for target_file, source in self.config["files"].items():
            strategy_icon = {"merge": "🔗", "patch": "🔧"}.get(source, "📄")

            print(f"   {strategy_icon} {target_file} ← {source}")


def main():
    """
    Main entry point for the overlay applicator.

    Command Line Usage:
        python apply-overlay.py [overlay_name] [--list] [--backup]

    Arguments:
        overlay_name: Name of overlay to apply (default: default)
        --list: List files without applying changes
        --backup: Create backup files before modification
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Apply environment-specific configuration overlays",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python apply-overlay.py default
    python apply-overlay.py production --backup
    python apply-overlay.py development --list
    
For more information, see the script documentation.
        """,
    )

    parser.add_argument(
        "overlay_name",
        nargs="?",
        default="default",
        help="Name of the overlay to apply (default: default)",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List affected files without applying changes",
    )

    parser.add_argument(
        "--backup", action="store_true", help="Create backup files before modification"
    )

    args = parser.parse_args()

    try:
        applicator = OverlayApplicator(args.overlay_name, create_backups=args.backup)

        if args.list:
            applicator.list_files()
        else:
            applicator.apply()

    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"❌ Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
