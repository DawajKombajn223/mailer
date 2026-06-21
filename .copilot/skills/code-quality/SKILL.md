# Code Quality Skill

## Cel
Narzędzia do formatowania, lintingu, type checking i ogólnej kontroli jakości kodu Python.

## Narzędzia

### 1. Black — Autoformatowanie kodu
```bash
# Formatuj bieżący plik
black mailer/email_sender.py

# Formatuj cały projekt
black .

# Sprawdź bez zmian
black --check .
```

**Reguły:**
- 88 znaków na linię (domyślnie)
- Automatyczne formatowanie stringów
- Spójne wcięcia

### 2. Flake8 — Linting (błędy, ostrzeżenia)
```bash
# Sprawdź cały projekt
flake8 .

# Sprawdź konkretny plik
flake8 mailer/subscribers.py

# Pokaż statystykę
flake8 . --statistics
```

**Reguły:**
- E501: Linia zbyt długa (80+ znaków)
- F401: Importy nieużywane
- E302: Brakuje 2 linii między definicjami
- W503: Operator na początku linii

### 3. Ruff — Szybki linter (alternatywa dla flake8)
```bash
# Linting
ruff check .

# Automatyczne poprawki
ruff check . --fix

# Formatowanie (ruff format)
ruff format .
```

**Zalety:**
- 10-100x szybszy niż flake8
- Wbudowana obsługa wielu reguł
- Automatyczne poprawki

### 4. mypy — Type Checking
```bash
# Sprawdzaj typy
mypy mailer/
mypy validators/
mypy tests/

# Tryb strict
mypy --strict mailer/
```

**Reguły:**
- Type hints są opcjonalne, ale zalecane
- Funkcje publiczne powinny mieć type hints
- Obiekty zwracane powinny mieć anotacje

### 5. isort — Sortowanie importów
```bash
# Sortuj importy w pliku
isort mailer/email_sender.py

# Sortuj wszystkie
isort .

# Sprawdź bez zmian
isort --check .
```

**Format importów:**
1. Standardowa biblioteka
2. Biblioteki zewnętrzne
3. Importy lokalne

## Automatyzacja

### Pre-commit hook (Quality checks)
Zapewnia, że kod przechodzi quality checks przed commitem:
```bash
# Zainstaluj
cp pre-commit-config.yaml .git/hooks/pre-push

# Przed każdym push:
# 1. black .
# 2. ruff check . --fix
# 3. mypy .
# 4. pytest
```

### GitHub Actions
Automatyczne quality checks na push/PR (możliwy setup)

## Workflow

### 1. Podczas kodowania
```bash
# Formatuj kod
black .

# Sortuj importy
isort .

# Sprawdzaj linter
flake8 .  # lub ruff check .

# Type checking
mypy .
```

### 2. Przed commitem
```bash
# Wszystko razem:
black . && isort . && ruff check . --fix && mypy . && pytest -q
```

### 3. Best Practices
- ✅ Zawsze formatuj (black) przed commitem
- ✅ Sortuj importy (isort)
- ✅ Usuń nieużywane importy (flake8: F401)
- ✅ Dodaj type hints dla funkcji publicznych
- ✅ Max 79 znaków na linię (dla docstringów)
- ✅ Max 88 znaków na linię (dla kodu)
- ✅ Unikaj linii dłuższych niż 100 znaków

## Konfiguracja

### pyproject.toml
```toml
[tool.black]
line-length = 88
target-version = ['py39']

[tool.ruff]
line-length = 88
select = ["E", "F", "W"]
ignore = ["E501", "W503"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
```

### .flake8
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,docs
```

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Black i flake8 się kłócą | Użyj black + ruff (kompatybilne) |
| Type hints zbyt restrykcyjne | Użyj `# type: ignore` dla wyjątków |
| Importy w złej kolejności | Uruchom `isort .` |
| Linia zbyt długa | Podziel na wiele linii lub użyj `# noqa: E501` |

## Linki
- Black: https://black.readthedocs.io/
- Flake8: https://flake8.pycqa.org/
- Ruff: https://docs.astral.sh/ruff/
- mypy: https://www.mypy-lang.org/
- isort: https://pycqa.github.io/isort/
