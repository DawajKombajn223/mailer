# Mailer Complete Testing Skill

## Komponenty do testowania

### 1. Email Validation
- Format email
- Długość
- Special characters

### 2. Email Sending
- Single recipient
- Multiple recipients
- Attachment handling
- Error handling

### 3. Subscribers Management
- Add subscriber
- Remove subscriber
- List subscribers
- Duplicate prevention

### 4. Web Interface (Flask)
- Routes accessibility
- Form validation
- Error handling
- HTML rendering

## Test Template

```python
import pytest
from unittest.mock import Mock, patch
from mailer.email_sender import EmailSender
from mailer.subscribers import SubscriberManager

class TestMailerComponent:
    @pytest.fixture
    def setup(self):
        # Setup fixture
        pass
    
    def test_happy_path(self, setup):
        # Main scenario
        pass
    
    def test_edge_cases(self, setup):
        # Edge cases
        pass
    
    def test_error_handling(self, setup):
        # Error scenarios
        pass
```

## Coverage Requirements
- Functions: 100%
- Branches: 80%
- Lines: 85%

## Tools
- pytest
- pytest-cov
- pytest-mock
- coverage
