# Flask Integration Skill

## Cel
Wspiera tworzenie i testowanie Flaskowych endpointów oraz web interface projektu Mailer.

## Zakres
- Routes accessibility
- Form validation
- HTML rendering
- Error handling
- Flash messages
- Session / cookies
- Integration z backendem mailera

## Przykład: Flask route

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from mailer.email_sender import EmailSender

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route('/send', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not email or not subject:
            flash('Email oraz temat są wymagane.', 'error')
            return redirect(url_for('send_email'))

        sender = EmailSender('smtp.example.com', 587)
        try:
            sender.send_email([email], subject, message)
            flash('Wiadomość została wysłana!', 'success')
        except Exception as e:
            flash(f'Błąd wysyłki: {e}', 'error')

    return render_template('send.html')
```

## Przykład: Test Flask

```python
import pytest
from flask import url_for

from app import app

class TestFlaskIntegration:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app.test_client()

    def test_send_page_loads(self, client):
        response = client.get('/send')
        assert response.status_code == 200
        assert b'Send email' in response.data

    def test_send_email_missing_fields(self, client):
        response = client.post('/send', data={})
        assert response.status_code == 302
```

## Reguły
- Testuj zarówno GET jak i POST
- Używaj `app.test_client()` do integracji
- Waliduj dane z formularzy po stronie serwera
- Unikaj prawdziwych połączeń SMTP w testach (mock)
- Sprawdzaj renderowanie szablonów i komunikaty flash

## Narzędzia
- pytest
- pytest-flask
- unittest.mock
- selenium / playwright (opcjonalnie)

## Użycie
```
@copilot use flask-integration skill
```
