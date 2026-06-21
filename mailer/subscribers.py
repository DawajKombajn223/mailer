"""Subscriber management module for Mailer project."""
from typing import List, Optional


class DuplicateSubscriberError(Exception):
    """Raised when trying to add duplicate subscriber."""
    pass


class SubscriberNotFoundError(Exception):
    """Raised when subscriber is not found."""
    pass


class SubscriberManager:
    """Manages email subscribers."""
    
    def __init__(self):
        """Initialize subscriber manager with empty subscribers list."""
        self._subscribers: List[dict] = []
    
    def add_subscriber(self, email: str, name: str = "", tags: List[str] = None) -> dict:
        """Add a new subscriber.
        
        Args:
            email: Subscriber email address
            name: Subscriber name (optional)
            tags: List of tags for subscriber (optional)
            
        Returns:
            The added subscriber dict
            
        Raises:
            DuplicateSubscriberError: If subscriber already exists
            ValueError: If email is empty
        """
        if not email:
            raise ValueError("Email cannot be empty")
        
        if self._find_by_email(email):
            raise DuplicateSubscriberError(f"Subscriber with email {email} already exists")
        
        subscriber = {
            'email': email.strip().lower(),
            'name': name,
            'tags': tags or [],
            'active': True
        }
        self._subscribers.append(subscriber)
        return subscriber
    
    def remove_subscriber(self, email: str) -> bool:
        """Remove a subscriber by email.
        
        Args:
            email: Subscriber email address
            
        Returns:
            True if removed, False otherwise
            
        Raises:
            SubscriberNotFoundError: If subscriber not found
        """
        sub = self._find_by_email(email)
        if not sub:
            raise SubscriberNotFoundError(f"Subscriber {email} not found")
        
        self._subscribers.remove(sub)
        return True
    
    def get_subscriber(self, email: str) -> Optional[dict]:
        """Get subscriber by email.
        
        Args:
            email: Subscriber email address
            
        Returns:
            Subscriber dict or None if not found
        """
        return self._find_by_email(email)
    
    def list_subscribers(self, active_only: bool = True) -> List[dict]:
        """List all subscribers.
        
        Args:
            active_only: If True, return only active subscribers
            
        Returns:
            List of subscriber dicts
        """
        if active_only:
            return [s for s in self._subscribers if s['active']]
        return self._subscribers.copy()
    
    def deactivate_subscriber(self, email: str) -> bool:
        """Deactivate a subscriber (soft delete).
        
        Args:
            email: Subscriber email address
            
        Returns:
            True if deactivated
            
        Raises:
            SubscriberNotFoundError: If subscriber not found
        """
        sub = self._find_by_email(email)
        if not sub:
            raise SubscriberNotFoundError(f"Subscriber {email} not found")
        
        sub['active'] = False
        return True
    
    def add_tags(self, email: str, tags: List[str]) -> dict:
        """Add tags to a subscriber.
        
        Args:
            email: Subscriber email address
            tags: Tags to add
            
        Returns:
            Updated subscriber dict
            
        Raises:
            SubscriberNotFoundError: If subscriber not found
        """
        sub = self._find_by_email(email)
        if not sub:
            raise SubscriberNotFoundError(f"Subscriber {email} not found")
        
        for tag in tags:
            if tag not in sub['tags']:
                sub['tags'].append(tag)
        
        return sub
    
    def get_subscribers_by_tag(self, tag: str) -> List[dict]:
        """Get subscribers with a specific tag.
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of subscribers with the tag
        """
        return [s for s in self._subscribers if tag in s['tags'] and s['active']]
    
    def count_subscribers(self, active_only: bool = True) -> int:
        """Count total subscribers.
        
        Args:
            active_only: If True, count only active subscribers
            
        Returns:
            Number of subscribers
        """
        return len(self.list_subscribers(active_only))
    
    def _find_by_email(self, email: str) -> Optional[dict]:
        """Find subscriber by email (case-insensitive).
        
        Args:
            email: Email to search for
            
        Returns:
            Subscriber dict or None
        """
        email_lower = email.strip().lower()
        for sub in self._subscribers:
            if sub['email'] == email_lower:
                return sub
        return None
