# Workflow: Tests Runner Agent

## Trigger
```
Run tests for mailer.email_sender
```

## Execution Flow

### Phase 1: Preparation (5-10s)
1. Sprawdź, czy istnieje `requirements.txt`
2. Upewnij się, że są zainstalowane zależności
3. Zidentyfikuj moduł lub folder do testowania

### Phase 2: Test Execution (10-20s)
1. Uruchom `pytest` dla wskazanego modułu/folderu
2. Dodaj `--cov=mailer --cov=validators --cov-report=term-missing`
3. Uchwyć wyniki i kody wyjścia

### Phase 3: Quality Checks (5-10s)
1. Uruchom `ruff check .` lub `flake8 .`
2. Uruchom `black --check .`
3. Uruchom `isort --check .`

### Phase 4: Report Generation (5-10s)
1. Przygotuj podsumowanie wyników testów
2. Zidentyfikuj niepowodzenia i brakujące pokrycie
3. Podaj rekomendacje poprawek

## Output
```
docs/test-reports/tests-summary.md
docs/test-reports/tests-details.md
```

## Success Criteria
- Wszystkie testy przechodzą
- Coverage: min. 80%
- Brak błędów lint
- Kod sformatowany
- Raport wygenerowany w `docs/test-reports/`
