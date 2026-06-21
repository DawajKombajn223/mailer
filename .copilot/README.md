# GitHub Copilot Configuration for Mailer

## Instrukcje (Instructions)
- `copilot-instructions.md` – Globalne standardy projektu, konwencje, wymagania bezpieczeństwa i testowania

## Skills (Umiejętności)

### 1. email-validation
**Ścieżka:** `.copilot/skills/email-validation/`

Wspiera walidację adresów email z testami.
- Pattern: EmailValidator z regex RFC 5322 (uproszczony)
- Testy: parametryzowane cases
- Topics: validation, email, regex, testing

Użycie:
```
@copilot use email-validation skill
```

### 2. mailer-complete-testing
**Ścieżka:** `.copilot/skills/mailer-testing/`

Kompleksowy skill dla testowania wszystkich komponentów mailera.
- Komponenty: Email Validation, Email Sending, Subscribers Management, Web Interface (Flask)
- Coverage: Functions 100%, Branches 80%, Lines 85%
- Narzędzia: pytest, pytest-cov, pytest-mock
- Template: Test fixtures, happy path, edge cases, error handling

Użycie:
```
@copilot use mailer-complete-testing skill
```

### 3. test-runner
**Ścieżka:** `.copilot/skills/test-runner/`

Automatyczne uruchamianie, monitorowanie i raportowanie testów.
- GUI Test Runner: `python test_runner_gui.py` (z coverage)
- File Watcher: `python .copilot/watch_tests.py` (automatyczne testy na zmianę pliku)
- Pre-commit hook: `.git/hooks/pre-commit` (testy przed commitem)
- CI/CD: GitHub Actions (`.github/workflows/tests.yml`)

Użycie:
```
@copilot use test-runner skill
```

### 4. code-quality
**Ścieżka:** `.copilot/skills/code-quality/`

Narzędzia do formatowania, lintingu, type checking i kontroli jakości kodu.
- Black — autoformatowanie (`black .`)
- Flake8 — linting (`flake8 .`)
- Ruff — szybki linter (`ruff check .`)
- mypy — type checking (`mypy .`)
- isort — sortowanie importów (`isort .`)
- Konfiguracja: `pyproject.toml`, `.flake8`

Użycie:
```
@copilot use code-quality skill
```

## Agenci (Agents)

### 1. Documentation Generator Agent
**Ścieżka:** `.agents/docs-generator-agent.yaml`

Autonomiczny agent generujący dokumentację dla projektu.
- Funkcje: Code analysis, documentation generation, example creation, test analysis
- Workflow: `.agents/docs-generator-workflow.md`
- Executor: `.agents/agent_executor.py` (Python-based)

Triggery:
```
Generate API documentation for [module]
Generate docs
Create documentation
Document this
```

## Workflow

### Typowy cykl pracy
1. **Developer pisze kod** – stosuje standardy z `copilot-instructions.md`
2. **Copilot sugeruje pattern** – z odpowiedniego skill (email-validation, testing, itd.)
3. **Dev generuje testy** – używając skill `mailer-complete-testing`
4. **Docs generator tworzy dokumentację** – executor agent
5. **Code reviews** – wspierane przez instrukcje i skill templates

### Generowanie dokumentacji
```bash
# Generuj docs dla modułu:
python .agents/agent_executor.py --module mailer.email_sender

# Generuj i uruchom testy:
python .agents/agent_executor.py --module validators --run-tests
```

### GUI Test Runner
```bash
# Uruchom graficzny runner testów (z coverage):
python test_runner_gui.py
```

### File Watcher (automatyczne testy)
```bash
# Terminal 2 - automatycznie uruchamia testy na zmianę pliku:
python .copilot/watch_tests.py
```

### Pre-commit Hook (testy przed commitem)
```bash
# Jednorazowo:
cp pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Od teraz, testy uruchomią się przed każdym commitem
git commit -m "feat: nowa funkcja"  # testy uruchamiają się automatycznie
```

### CI/CD (GitHub Actions)
Testy uruchamiają się automatycznie na push/PR:
- `.github/workflows/tests.yml`
- Python 3.9, 3.12, 3.13
- Coverage report do Codecov

## Best Practices

### Zawsze
- ✅ Zawsze zapoznaj się z `copilot-instructions.md` przed rozpoczęciem
- ✅ Użyj odpowiedniego skill jeśli dostępny (email-validation, mailer-testing, test-runner, code-quality)
- ✅ Minimalne pokrycie testów: 80% (coverage)
- ✅ Type hints dla kodu Python
- ✅ PEP 8 — 4 spacje, max 79 znaków
- ✅ Code formatting: `black .` + `isort .`
- ✅ Linting: `flake8 .` lub `ruff check .`
- ✅ Type checking: `mypy .`
- ✅ Mockuj usługi zewnętrzne (SMTP, DB)
- ✅ Każda funkcja: min. 2 testy (happy path + edge cases)

### Dla bardziej złożonych zadań
- 🤖 Używaj agentów (Documentation Generator Agent)
- 📄 Dla multi-step tasków, wygeneruj dokumentację automatycznie
- 🔍 Zawsze weryfikuj wygenerowaną dokumentację

### Struktura projektu
```
.copilot/
├── README.md                           ← Czytaj najpierw!
├── copilot-instructions.md             ← Globalne standardy
├── watch_tests.py                      ← File watcher (auto testy)
└── skills/
    ├── email-validation/
    │   ├── SKILL.md
    │   └── .promptyaml
    ├── mailer-testing/
    │   ├── SKILL.md
    │   └── .promptyaml
    ├── test-runner/
    │   ├── SKILL.md
    │   └── .promptyaml
    └── code-quality/
        ├── SKILL.md
        └── .promptyaml

.github/
└── workflows/
    └── tests.yml                       ← GitHub Actions CI/CD

.agents/
├── agent_executor.py                   ← Executor dla dokumentacji
├── docs-generator-agent.yaml           ← Konfiguracja agenta
└── docs-generator-workflow.md          ← Workflow agenta

tests/
├── test_email_validator.py
├── test_email_sender.py
└── test_subscribers.py

docs/                                    ← Wygenerowana dokumentacja
├── api/
│   ├── mailer.md
│   ├── mailer_email_sender.md
│   ├── mailer_subscribers.md
│   └── validators.md
└── examples/
    ├── mailer_usage.md
    ├── mailer_email_sender_usage.md
    ├── mailer_subscribers_usage.md
    └── validators_usage.md

mailer/
├── __init__.py
├── email_sender.py
└── subscribers.py

validators/
└── __init__.py

test_runner_gui.py                      ← Graficzny test runner z coverage
pre-commit-hook.sh                      ← Pre-commit hook (zainstaluj do .git/hooks/)
copilot-instructions.md                 ← Główne instrukcje (również powyżej)
pyproject.toml                          ← Konfiguracja black, ruff, mypy, isort
.flake8                                 ← Konfiguracja flake8
requirements.txt                         ← pytest, pytest-cov, pytest-mock, black, flake8, ruff, mypy, isort
```

## Linki do dokumentacji

- **Instrukcje główne:** [copilot-instructions.md](../copilot-instructions.md)
- **Email Validation Skill:** [skills/email-validation/SKILL.md](skills/email-validation/SKILL.md)
- **Mailer Testing Skill:** [skills/mailer-testing/SKILL.md](skills/mailer-testing/SKILL.md)
- **Docs Generator:** [../.agents/docs-generator-agent.yaml](../.agents/docs-generator-agent.yaml)
- **Executor:** [../.agents/agent_executor.py](../.agents/agent_executor.py)

## FAQ

### Jak dodać nowy skill?
1. Stwórz folder `.copilot/skills/<skill-name>/`
2. Dodaj `.promptyaml` (konfiguracja) i `SKILL.md` (dokumentacja)
3. Odwołaj się w `copilot-instructions.md`

### Jak uruchomić testy?
```bash
python -m pytest -q --cov=mailer --cov=validators --cov-report=term-missing
```

### Jak wygenerować dokumentację?
```bash
python .agents/agent_executor.py --module mailer
python .agents/agent_executor.py --module validators
```

### Jak uruchomić GUI test runner?
```bash
python test_runner_gui.py
```

### Jak formatować kod?
```bash
# Formatuj (black + isort)
black . && isort .

# Sprawdzaj linter
flake8 .  # lub ruff check .

# Type checking
mypy .
```

### Szybki quality check (wszystko)
```bash
black . && isort . && flake8 . && mypy . && pytest -q
```

## Kontakt & Issues
- Zaktualizuj README.md jeśli dodajesz nowy skill lub agenta
- Raportuj problemy w repozytorium
- Sugeruj ulepszenia poprzez pull requests

---

**Ostatnia aktualizacja:** 2026-06-21  
**Version:** 1.0
