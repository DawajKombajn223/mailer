# GitHub Copilot Instructions - Mailer Project

## 1. Python i Zależności
- Python 3.12+ (lub co najmniej 3.9+ zgodnie z kompatybilnością projektu)
- Wymagane biblioteki: `Flask`, `pytest`, `pytest-cov`, `python-dotenv`, `email-validator` lub podobne
- Zarządzaj zależnościami w `requirements.txt` lub `pyproject.toml`
- Używaj formatowania i lintingu: `black`, `flake8`, `ruff`
- Type hints są zalecane, tam gdzie mają sens

## 2. Standardy PEP 8
- Stosuj PEP 8 w całym kodzie Python
- 4 spacje zamiast tabulatorów
- Maksymalna długość linii: 79 znaków dla kodu, 72 dla komentarzy i dokumentacji
- Używaj czytelnych importów: standardowa biblioteka, biblioteki zewnętrzne, importy lokalne
- Utrzymuj moduły w rozsądnej długości: maksimum 500 linii
- Funkcje powinny być krótkie i zwięzłe: maksimum 50 linii
- Klasy powinny mieć pojedynczą odpowiedzialność

## 3. Konwencje nazewnicze
- Pliki i moduły: `snake_case`
- Klasy: `PascalCase`
- Funkcje i metody: `snake_case`
- Zmienne i argumenty: `snake_case`
- Stałe: `UPPER_SNAKE_CASE`
- Szablony HTML: opisowe nazwy, np. `email_confirmation.html`, `newsletter.html`
- Zasoby statyczne: `styles.css`, `main.js`, `mailer.js`
- Testy: `test_<moduł>.py`, funkcje testowe `test_<scenariusz>()`

## 4. Wymagania testowania
- Minimalne pokrycie: 80% code coverage
- Używaj `pytest` wraz z `pytest-cov`
- Testuj wszystkie istotne części aplikacji:
  - `mailer/` – logika biznesowa, walidacja, obsługa wyjątków
  - `templates/` – renderowanie szablonów HTML, poprawność danych wejściowych
  - `static/` – struktura zasobów, integracja z Flask
  - `tests/` – testy jednostkowe, integracyjne, fixture
- Mockuj zewnętrzne usługi: SMTP, bazy danych i inne połączenia sieciowe
- Testy muszą być szybkie, deterministyczne i samodzielne

## 5. Bezpieczeństwo
- Nigdy nie przechowuj poświadczeń ani sekretów w repozytorium
- Environment variables dla secrets i konfiguracji (SMTP, API keys, tryb debugowania)
- Używaj `.env.example` do dokumentacji zmiennych środowiskowych, a `.env` dodaj do `.gitignore`
- Waliduj input użytkownika, zwłaszcza adresy e-mail
- Unikaj wstrzykiwania surowych danych do szablonów i treści wiadomości
- Ogranicz logowanie wrażliwych danych

## 6. Konwencje commitów i Git
- Używaj konwencji `conventional commits`
- Przykłady:
  - `feat: dodaj moduł wysyłki e-mail`
  - `fix: napraw walidację adresu e-mail`
  - `refactor: uprość logikę obsługi błędów`
  - `test: dodaj testy dla modułu SMTP`
  - `docs: uaktualnij instrukcję konfiguracji`
- Nazwy branchy:
  - `feature/*`
  - `bugfix/*`
  - `docs/*`
- PR: opisany w propozycji, z odniesieniem do testów i zmian

## 7. Obsługa błędów
- Problemy powinny być zgłaszane w sposób czytelny, bez ujawniania wewnętrznych szczegółów
- Loguj szczegóły błędów po stronie serwera
- Obsługuj typowe problemy:
  - błędny adres e-mail
  - brak połączenia SMTP
  - błędy ładowania szablonów
  - brak wymaganych zmiennych środowiskowych
- Stosuj dedykowane wyjątki, np. `EmailValidationError`, `SmtpConnectionError`
- Unikaj „cichego” pomijania wyjątków; zgłaszaj je lub odpowiednio obsługuj

## 8. Komponenty projektu
- `mailer/` – logika biznesowa i obsługa wysyłki wiadomości. Oddziel konfigurację od kodu biznesowego.
- `templates/` – szablony Flask HTML. Używaj bezpiecznego renderowania i semantycznych elementów.
- `static/` – zasoby CSS/JavaScript. Organizuj pliki tak, aby łatwo było je odnaleźć i aktualizować.
- `tests/` – testy `pytest` i testy integracyjne. Utrzymuj jasną strukturę i fixture do wspólnych ustawień.

---

Ten plik stanowi wytyczne dla zespołu pracującego nad projektem Mailer. Aktualizuj go, gdy projekt się rozwija lub gdy pojawiają się nowe wymagania.
