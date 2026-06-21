"""Tests for subscribers module."""

import pytest
from mailer.subscribers import (
    SubscriberManager,
    DuplicateSubscriberError,
    SubscriberNotFoundError,
)


class TestSubscriberManagerAdd:
    """Tests for adding subscribers."""

    @pytest.fixture
    def manager(self):
        return SubscriberManager()

    def test_add_subscriber_success(self, manager):
        """Test adding a new subscriber."""
        subscriber = manager.add_subscriber("user@example.com", "John Doe")

        assert subscriber["email"] == "user@example.com"
        assert subscriber["name"] == "John Doe"
        assert subscriber["active"] is True
        assert subscriber["tags"] == []

    def test_add_subscriber_with_tags(self, manager):
        """Test adding subscriber with tags."""
        subscriber = manager.add_subscriber(
            "user@example.com", "John", tags=["newsletter", "vip"]
        )

        assert "newsletter" in subscriber["tags"]
        assert "vip" in subscriber["tags"]

    def test_add_subscriber_duplicate(self, manager):
        """Test adding duplicate subscriber raises error."""
        manager.add_subscriber("user@example.com", "John")

        with pytest.raises(DuplicateSubscriberError):
            manager.add_subscriber("user@example.com", "John")

    def test_add_subscriber_case_insensitive(self, manager):
        """Test email is case-insensitive."""
        manager.add_subscriber("USER@EXAMPLE.COM", "John")

        with pytest.raises(DuplicateSubscriberError):
            manager.add_subscriber("user@example.com", "Jane")

    def test_add_subscriber_empty_email(self, manager):
        """Test adding subscriber with empty email raises error."""
        with pytest.raises(ValueError):
            manager.add_subscriber("", "John")

    def test_add_subscriber_whitespace_trim(self, manager):
        """Test email whitespace is trimmed."""
        subscriber = manager.add_subscriber("  user@example.com  ", "John")
        assert subscriber["email"] == "user@example.com"


class TestSubscriberManagerRemove:
    """Tests for removing subscribers."""

    @pytest.fixture
    def manager(self):
        mgr = SubscriberManager()
        mgr.add_subscriber("user1@example.com")
        mgr.add_subscriber("user2@example.com")
        return mgr

    def test_remove_subscriber_success(self, manager):
        """Test removing an existing subscriber."""
        result = manager.remove_subscriber("user1@example.com")

        assert result is True
        assert manager.get_subscriber("user1@example.com") is None

    def test_remove_subscriber_not_found(self, manager):
        """Test removing non-existent subscriber raises error."""
        with pytest.raises(SubscriberNotFoundError):
            manager.remove_subscriber("nonexistent@example.com")


class TestSubscriberManagerList:
    """Tests for listing subscribers."""

    @pytest.fixture
    def manager(self):
        mgr = SubscriberManager()
        mgr.add_subscriber("user1@example.com", "User 1")
        mgr.add_subscriber("user2@example.com", "User 2")
        mgr.add_subscriber("user3@example.com", "User 3")
        return mgr

    def test_list_subscribers_all(self, manager):
        """Test listing all subscribers."""
        subscribers = manager.list_subscribers(active_only=False)

        assert len(subscribers) == 3

    def test_list_subscribers_active_only(self, manager):
        """Test listing only active subscribers."""
        manager.deactivate_subscriber("user3@example.com")
        subscribers = manager.list_subscribers(active_only=True)

        assert len(subscribers) == 2

    def test_count_subscribers(self, manager):
        """Test counting subscribers."""
        count = manager.count_subscribers()
        assert count == 3

    def test_count_subscribers_active_only(self, manager):
        """Test counting only active subscribers."""
        manager.deactivate_subscriber("user1@example.com")
        count = manager.count_subscribers(active_only=True)

        assert count == 2


class TestSubscriberManagerDeactivate:
    """Tests for deactivating subscribers."""

    @pytest.fixture
    def manager(self):
        mgr = SubscriberManager()
        mgr.add_subscriber("user@example.com")
        return mgr

    def test_deactivate_subscriber_success(self, manager):
        """Test deactivating a subscriber."""
        result = manager.deactivate_subscriber("user@example.com")

        assert result is True
        subscriber = manager.get_subscriber("user@example.com")
        assert subscriber["active"] is False

    def test_deactivate_subscriber_not_found(self, manager):
        """Test deactivating non-existent subscriber raises error."""
        with pytest.raises(SubscriberNotFoundError):
            manager.deactivate_subscriber("nonexistent@example.com")

    def test_deactivate_subscriber_not_in_list(self, manager):
        """Test deactivated subscriber not in active list."""
        manager.deactivate_subscriber("user@example.com")
        active = manager.list_subscribers(active_only=True)

        assert len(active) == 0


class TestSubscriberManagerTags:
    """Tests for tag management."""

    @pytest.fixture
    def manager(self):
        mgr = SubscriberManager()
        mgr.add_subscriber("user1@example.com", tags=["newsletter"])
        mgr.add_subscriber("user2@example.com", tags=["vip"])
        mgr.add_subscriber("user3@example.com", tags=["newsletter", "vip"])
        return mgr

    def test_add_tags_success(self, manager):
        """Test adding tags to subscriber."""
        subscriber = manager.add_tags("user1@example.com", ["vip"])

        assert "newsletter" in subscriber["tags"]
        assert "vip" in subscriber["tags"]

    def test_add_tags_avoid_duplicate(self, manager):
        """Test adding duplicate tags is avoided."""
        subscriber = manager.add_tags("user1@example.com", ["newsletter"])

        # Count occurrences of 'newsletter'
        newsletter_count = subscriber["tags"].count("newsletter")
        assert newsletter_count == 1

    def test_get_subscribers_by_tag(self, manager):
        """Test getting subscribers by tag."""
        newsletter_subs = manager.get_subscribers_by_tag("newsletter")

        assert len(newsletter_subs) == 2
        emails = [s["email"] for s in newsletter_subs]
        assert "user1@example.com" in emails
        assert "user3@example.com" in emails

    def test_get_subscribers_by_tag_not_found(self, manager):
        """Test getting subscribers by non-existent tag."""
        subs = manager.get_subscribers_by_tag("nonexistent")

        assert len(subs) == 0

    def test_get_subscribers_by_tag_excludes_inactive(self, manager):
        """Test tag search excludes inactive subscribers."""
        manager.deactivate_subscriber("user1@example.com")
        newsletter_subs = manager.get_subscribers_by_tag("newsletter")

        assert len(newsletter_subs) == 1
        assert newsletter_subs[0]["email"] == "user3@example.com"


class TestSubscriberManagerGet:
    """Tests for getting individual subscribers."""

    @pytest.fixture
    def manager(self):
        mgr = SubscriberManager()
        mgr.add_subscriber("user@example.com", "John")
        return mgr

    def test_get_subscriber_success(self, manager):
        """Test getting an existing subscriber."""
        subscriber = manager.get_subscriber("user@example.com")

        assert subscriber is not None
        assert subscriber["email"] == "user@example.com"
        assert subscriber["name"] == "John"

    def test_get_subscriber_not_found(self, manager):
        """Test getting non-existent subscriber returns None."""
        subscriber = manager.get_subscriber("nonexistent@example.com")

        assert subscriber is None

    def test_get_subscriber_case_insensitive(self, manager):
        """Test subscriber retrieval is case-insensitive."""
        subscriber = manager.get_subscriber("USER@EXAMPLE.COM")

        assert subscriber is not None
