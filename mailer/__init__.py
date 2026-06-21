"""Mailer package - email sending and subscriber management."""

from .email_sender import EmailSender, EmailValidationError, SmtpConnectionError
from .subscribers import SubscriberManager, DuplicateSubscriberError, SubscriberNotFoundError

__all__ = [
    'EmailSender',
    'EmailValidationError',
    'SmtpConnectionError',
    'SubscriberManager',
    'DuplicateSubscriberError',
    'SubscriberNotFoundError',
]
