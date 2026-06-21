# API: mailer.email_sender

Email sending module for Mailer project.

## Classes

### EmailValidationError

Raised when email validation fails.

### SmtpConnectionError

Raised when SMTP connection fails.

### EmailSender

Sends emails via SMTP server.

#### validate_email

```python
def validate_email() -> bool
```

Validate email format.

Args:
    email: Email address to validate
    
Returns:
    True if valid, False otherwise

#### send_email

```python
def send_email(to: List[str], subject: str, body: str, html: bool) -> bool
```

Send email to one or more recipients.

Args:
    to: List of recipient email addresses
    subject: Email subject
    body: Email body
    html: Whether body is HTML format
    
Returns:
    True if email sent successfully
    
Raises:
    EmailValidationError: If recipient email is invalid
    SmtpConnectionError: If SMTP connection fails

#### send_bulk_email

```python
def send_bulk_email(recipients: List[str], subject: str, body: str, html: bool) -> dict
```

Send email to multiple recipients with individual tracking.

Args:
    recipients: List of recipient emails
    subject: Email subject
    body: Email body
    html: Whether body is HTML
    
Returns:
    Dict with 'sent' and 'failed' lists

## Examples

Basic usage example to be filled in by the agent.
