# Konfiguracja zewnętrznego dostawcy tożsamości dla Google

## Krok 1: Utworzenie klienta Google OAuth 2.0

1. Przejdź do Konsoli Deweloperów Google.
2. Utwórz nowy projekt lub wybierz istniejący.
3. Przejdź do sekcji "Poświadczenia", następnie kliknij "Utwórz poświadczenia" i wybierz "Identyfikator klienta OAuth".
4. Skonfiguruj ekran zgody, jeśli zostaniesz o to poproszony.
5. Dla typu aplikacji wybierz "Aplikacja internetowa".
6. Na razie pozostaw pole przekierowania URI pustym, aby ustawić je później, i tymczasowo zapisz.[Patrz Krok 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Po utworzeniu zanotuj identyfikator klienta i klucz tajny klienta.

Aby uzyskać więcej szczegółów, odwiedź [oficjalny dokument Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Krok 2: Przechowywanie poświadczeń Google OAuth w AWS Secrets Manager

1. Przejdź do konsoli AWS Management Console.
2. Przejdź do Secrets Manager i wybierz "Przechowaj nowy sekret".
3. Wybierz "Inny typ sekretu".
4. Wprowadź identyfikator klienta Google OAuth (clientId) i sekret klienta (clientSecret) jako pary klucz-wartość.

   1. Klucz: clientId, Wartość: <YOUR_GOOGLE_CLIENT_ID>
   2. Klucz: clientSecret, Wartość: <YOUR_GOOGLE_CLIENT_SECRET>

5. Postępuj zgodnie z monitami, aby nazwać i opisać sekret. Zanotuj nazwę sekretu, ponieważ będzie potrzebna w kodzie CDK. Na przykład, googleOAuthCredentials. (Użyj w nazwie zmiennej w Kroku 3 <YOUR_SECRET_NAME>)
6. Przejrzyj i zapisz sekret.

### Uwaga

Nazwy kluczy muszą dokładnie odpowiadać ciągom 'clientId' i 'clientSecret'.

## Krok 3: Aktualizacja pliku cdk.json

W pliku cdk.json dodaj dostawcę tożsamości i nazwę sekretu.

w następujący sposób:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<TWOJA_NAZWA_SEKRETU>"
      }
    ],
    "userPoolDomainPrefix": "<UNIKALNY_PREFIKS_DOMENY_DLA_TWOJEJ_PULI_UŻYTKOWNIKÓW>"
  }
}
```

### Uwaga

#### Unikalność

Prefiks userPoolDomainPrefix musi być globalnie unikalny we wszystkich użytkownikach Amazon Cognito. Jeśli wybierzesz prefiks, który jest już używany przez inne konto AWS, utworzenie domeny puli użytkowników zakończy się niepowodzeniem. Dobrą praktyką jest uwzględnienie identyfikatorów, nazw projektów lub nazw środowisk w prefiksie, aby zapewnić unikalność.

## Krok 4: Wdrożenie stosu CDK

Wdróż swój stos CDK w AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Krok 5: Aktualizacja klienta Google OAuth adresami URL przekierowania Cognito

Po wdrożeniu stosu, AuthApprovedRedirectURI pojawi się w danych wyjściowych CloudFormation. Wróć do konsoli Google Developer Console i zaktualizuj klienta OAuth o prawidłowe adresy URL przekierowania.