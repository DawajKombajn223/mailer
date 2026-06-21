# Workflow: Documentation Generation Agent

## Trigger
```
Użytkownik: "Generate API documentation for mailer.subscribers module"
```

## Execution Flow

### Phase 1: Analysis (10-15s)
1. Przeczytaj `mailer/subscribers.py`
2. Przeanalizuj strukturę klas i funkcji
3. Wyciągnij docstrings i type hints
4. Identyfikuj eksportowane API

### Phase 2: Context Gathering (5-10s)
1. Przeczytaj `tests/test_subscribers.py`
2. Poszukaj usage patterns
3. Zbierz informacje o zależnościach
4. Sprawdź README dla kontekstu

### Phase 3: Generation (10-20s)
1. Stwórz strukturę dokumentacji
2. Konwertuj docstrings na Markdown
3. Dodaj type hints do sygnatury
4. Generuj tabelę API

### Phase 4: Examples (15-30s)
1. Stwórz Basic Usage example
2. Dodaj Advanced Usage patterns
3. Dołącz Error Handling example
4. Utwórz Complete Working Example

### Phase 5: Validation (5-10s)
1. Waliduj Markdown syntax
2. Sprawdź completeness
3. Weryfikuj code snippets
4. Zakończ z summary

## Output
```
docs/api/subscribers.md
docs/examples/subscribers_usage.md
docs/CHANGELOG.md (updated)
```

## Success Criteria
- Wszystkie funkcje dokumentowane
- Wszystkie parametry opisane
- Type hints pokazane
- Min. 5 examples
- Markdown valid
