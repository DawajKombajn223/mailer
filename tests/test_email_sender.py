"""Tests for email_sender module."""

import pytest
from unittest.mock import MagicMock, patch

from mailer.email_sender import (
    EmailSender,
    EmailValidationError,
    SmtpConnectionError,
)


class TestEmailSenderValidation:
    """Tests for email validation."""

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("user@example.com", True),
            ("user+tag@domain.co.uk", True),
            ("test.email@sub.domain.org", True),
            ("invalid@", False),
            ("@domain.com", False),
            ("user", False),
            ("", False),
            (None, False),
            ("user@domain", False),
            ("user space@domain.com", False),
        ],
    )
    def test_validate_email(self, email, expected):
        """Test email validation with various formats."""
        assert EmailSender.validate_email(email) == expected

    def test_validate_email_with_whitespace(self):
        """Test email validation with leading/trailing whitespace."""
        assert EmailSender.validate_email("  user@example.com  ") is True


class TestEmailSenderInit:
    """Tests for EmailSender initialization."""

    def test_init_with_credentials(self):
        """Test initialization with SMTP credentials."""
        sender = EmailSender("smtp.gmail.com", 587, "user@gmail.com", "password")
        assert sender.smtp_host == "smtp.gmail.com"
        assert sender.smtp_port == 587
        assert sender.username == "user@gmail.com"
        assert sender.password == "password"

    def test_init_without_credentials(self):
        """Test initialization without credentials."""
        sender = EmailSender("localhost", 25)
        assert sender.smtp_host == "localhost"
        assert sender.smtp_port == 25
        assert sender.username is None
        assert sender.password is None


class TestEmailSenderSendEmail:
    """Tests for sending single emails."""

    @pytest.fixture
    def sender(self):
        return EmailSender("smtp.example.com", 587, "sender@example.com", "pass")

    def test_send_email_success(self, sender):
        """Test successful email sending."""
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = sender.send_email(
                to=["recipient@example.com"], subject="Test", body="Test body"
            )

            assert result is True
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("sender@example.com", "pass")
            mock_server.send_message.assert_called_once()

    def test_send_email_no_recipients(self, sender):
        """Test sending email with no recipients raises error."""
        with pytest.raises(EmailValidationError):
            sender.send_email(to=[], subject="Test", body="Test")

    def test_send_email_invalid_recipient(self, sender):
        """Test sending email to invalid recipient raises error."""
        with pytest.raises(EmailValidationError):
            sender.send_email(to=["invalid-email"], subject="Test", body="Test")

    def test_send_email_multiple_recipients(self, sender):
        """Test sending email to multiple recipients."""
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = sender.send_email(
                to=["user1@example.com", "user2@example.com"],
                subject="Test",
                body="Test body",
            )

            assert result is True

    def test_send_email_html_format(self, sender):
        """Test sending HTML email."""
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = sender.send_email(
                to=["recipient@example.com"],
                subject="Test",
                body="<h1>Test</h1>",
                html=True,
            )

            assert result is True

    def test_send_email_smtp_error(self, sender):
        """Test handling SMTP errors."""
        with patch("smtplib.SMTP") as mock_smtp:
            mock_smtp.return_value.__enter__.side_effect = Exception("SMTP failed")

            with pytest.raises(SmtpConnectionError):
                sender.send_email(
                    to=["recipient@example.com"], subject="Test", body="Test"
                )


class TestEmailSenderBulkEmail:
    """Tests for bulk email sending."""

    @pytest.fixture
    def sender(self):
        return EmailSender("smtp.example.com", 587, "sender@example.com", "pass")

    def test_send_bulk_email_all_success(self, sender):
        """Test bulk sending with all emails successful."""
        with patch.object(sender, "send_email", return_value=True):
            result = sender.send_bulk_email(
                recipients=["user1@example.com", "user2@example.com"],
                subject="Test",
                body="Test",
            )

            assert len(result["sent"]) == 2
            assert len(result["failed"]) == 0

    def test_send_bulk_email_partial_failure(self, sender):
        """Test bulk sending with some failures."""

        def send_email_side_effect(to, subject, body, html=False):
            if "invalid" in to[0]:
                raise EmailValidationError("Invalid email")
            return True

        with patch.object(sender, "send_email", side_effect=send_email_side_effect):
            result = sender.send_bulk_email(
                recipients=["user@example.com", "invalid@email"],
                subject="Test",
                body="Test",
            )

            assert len(result["sent"]) == 1
            assert len(result["failed"]) == 1

    def test_send_bulk_email_empty_list(self, sender):
        """Test bulk sending with empty recipient list."""
        result = sender.send_bulk_email(recipients=[], subject="Test", body="Test")

        assert len(result["sent"]) == 0
        assert len(result["failed"]) == 0
