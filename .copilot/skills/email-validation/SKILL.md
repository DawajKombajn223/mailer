# Email Validation Skill

## Cel umiejętności
Wspieranie tworzenia funkcji walidacji emaili z testami.

## Kontekst
- Projekt: Mailer
- Wymaganie: Walidacja subskrybentów
- Standard: RFC 5322 (uproszczony)

## Wzorzec: Walidator Email

```python
import re

class EmailValidator:
    # Pattern: user@domain.com
    PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate(email: str) -> bool:
        """Waliduj format emaila."""
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(EmailValidator.PATTERN, email.strip()))
```

## Wzorzec: Testy

```python
import pytest
from validators import EmailValidator

class TestEmailValidator:
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("user+tag@domain.co.uk", True),
        ("invalid@", False),
        ("@domain.com", False),
        ("user", False),
        ("", False),
    ])
    def test_email_validation(self, email, expected):
        assert EmailValidator.validate(email) == expected
```

## Reguły
- Patrz patterns RFC 5322
- Waliduj zarówno format jak i długość
- Nie wysyłaj emaili w walidacji (tylko format)
- Testy: parametryzowane cases
