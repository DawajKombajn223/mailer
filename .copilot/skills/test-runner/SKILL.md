# Test Runner Skill

## Cel
Automatyczne uruchamianie, monitorowanie i raportowanie testów.

## Funkcje

### 1. Szybkie uruchomienie testów
Komendy:
```bash
# Wszystkie testy (quick)
python -m pytest -q

# Z verbose output
python -m pytest -v

# Z coverage report
python -m pytest -q --cov=mailer --cov=validators --cov-report=term-missing
```

### 2. Testy specyficznych plików
```bash
python -m pytest tests/test_email_sender.py -v
python -m pytest tests/test_subscribers.py::TestSubscriberManagerAdd -v
```

### 3. Testy z failfast (stop na pierwszym błędzie)
```bash
python -m pytest -x  # stop na pierwszym błędzie
python -m pytest -x -v
```

### 4. GUI Test Runner
```bash
python test_runner_gui.py
```
Wyświetla:
- Listę plików testowych
- Uruchamianie wybranych/wszystkich testów
- Coverage report (term-missing)
- Integracja z docs generator

## Automatyzacja

### Pre-commit hook
Umieszcz `.git/hooks/pre-commit` aby testy uruchamiały się przed commitem:
```bash
#!/bin/bash
python -m pytest -q --tb=short
```

### Watcher script
Umiędzy pracy w terminal 2 (file watcher):
```bash
python .copilot/watch_tests.py
```
Automatycznie uruchamia testy gdy plik się zmieni.

## Coverage Requirements
- Minimum: 80%
- Target: 90%
- Ideal: 95%+

Zabudne linie: `# pragma: no cover`

## Best Practices
1. **Zawsze testuj przed pushem** — użyj pre-commit hook
2. **Monitoruj coverage** — target 80% minimum
3. **Szybkie feedback** — używaj `-x` dla failfast
4. **Parametryzuj testy** — `@pytest.mark.parametrize`
5. **Mockuj usługi** — nie wysyłaj rzeczywistych emaili

## Fixtures

Za najczęściej używane:
```python
@pytest.fixture
def sender():
    return EmailSender("smtp.test", 587, "user", "pass")

@pytest.fixture
def manager():
    return SubscriberManager()
```

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Testy się nie uruchamiają | `pip install -r requirements.txt` |
| Coverage nie pokazuje się | `pip install pytest-cov` |
| ModuleNotFoundError | Upewnij się że jesteś w katalogu `hello` |
| GUI nie uruchamia się | Tkinter powinien być preinstalowany; na WSL: `apt install python3-tk` |

## Integracja z CI (GitHub Actions)
Zobacz `.github/workflows/tests.yml` (do stworzenia)
