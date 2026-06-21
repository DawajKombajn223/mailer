# API: mailer.subscribers

Subscriber management module for Mailer project.

## Classes

### DuplicateSubscriberError

Raised when trying to add duplicate subscriber.

### SubscriberNotFoundError

Raised when subscriber is not found.

### SubscriberManager

Manages email subscribers.

#### add_subscriber

```python
def add_subscriber(email: str, name: str, tags: List[str]) -> dict
```

Add a new subscriber.

Args:
    email: Subscriber email address
    name: Subscriber name (optional)
    tags: List of tags for subscriber (optional)
    
Returns:
    The added subscriber dict
    
Raises:
    DuplicateSubscriberError: If subscriber already exists
    ValueError: If email is empty

#### remove_subscriber

```python
def remove_subscriber(email: str) -> bool
```

Remove a subscriber by email.

Args:
    email: Subscriber email address
    
Returns:
    True if removed, False otherwise
    
Raises:
    SubscriberNotFoundError: If subscriber not found

#### get_subscriber

```python
def get_subscriber(email: str) -> Optional[dict]
```

Get subscriber by email.

Args:
    email: Subscriber email address
    
Returns:
    Subscriber dict or None if not found

#### list_subscribers

```python
def list_subscribers(active_only: bool) -> List[dict]
```

List all subscribers.

Args:
    active_only: If True, return only active subscribers
    
Returns:
    List of subscriber dicts

#### deactivate_subscriber

```python
def deactivate_subscriber(email: str) -> bool
```

Deactivate a subscriber (soft delete).

Args:
    email: Subscriber email address
    
Returns:
    True if deactivated
    
Raises:
    SubscriberNotFoundError: If subscriber not found

#### add_tags

```python
def add_tags(email: str, tags: List[str]) -> dict
```

Add tags to a subscriber.

Args:
    email: Subscriber email address
    tags: Tags to add
    
Returns:
    Updated subscriber dict
    
Raises:
    SubscriberNotFoundError: If subscriber not found

#### get_subscribers_by_tag

```python
def get_subscribers_by_tag(tag: str) -> List[dict]
```

Get subscribers with a specific tag.

Args:
    tag: Tag to filter by
    
Returns:
    List of subscribers with the tag

#### count_subscribers

```python
def count_subscribers(active_only: bool) -> int
```

Count total subscribers.

Args:
    active_only: If True, count only active subscribers
    
Returns:
    Number of subscribers

#### _find_by_email

```python
def _find_by_email(email: str) -> Optional[dict]
```

Find subscriber by email (case-insensitive).

Args:
    email: Email to search for
    
Returns:
    Subscriber dict or None

## Examples

Basic usage example to be filled in by the agent.
