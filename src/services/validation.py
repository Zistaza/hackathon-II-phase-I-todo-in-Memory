"""
Validation service for priority and tag format validation.
Provides reusable validation functions for task attributes.
"""

from typing import List
from src.exceptions import TaskValidationError


def validate_priority(priority: str) -> None:
    """
    Validate priority value is one of the allowed values.

    Args:
        priority: Priority value to validate

    Raises:
        TaskValidationError: If priority is not one of 'high', 'medium', 'low'
    """
    valid_priorities = ['high', 'medium', 'low']
    if priority not in valid_priorities:
        raise TaskValidationError(f"Priority must be one of: {', '.join(valid_priorities)}, got: {priority}")


def validate_tags(tags: List[str]) -> None:
    """
    Validate tags format - each tag must be non-empty and contain no spaces.

    Args:
        tags: List of tags to validate

    Raises:
        TaskValidationError: If any tag is invalid
    """
    for tag in tags:
        if not tag or not tag.strip():
            raise TaskValidationError(f"Tag cannot be empty: '{tag}'")
        if ' ' in tag:
            raise TaskValidationError(f"Tag cannot contain spaces: '{tag}'")


def validate_tag(tag: str) -> None:
    """
    Validate a single tag format.

    Args:
        tag: Tag to validate

    Raises:
        TaskValidationError: If tag is invalid
    """
    if not tag or not tag.strip():
        raise TaskValidationError(f"Tag cannot be empty: '{tag}'")
    if ' ' in tag:
        raise TaskValidationError(f"Tag cannot contain spaces: '{tag}'")


def validate_search_keyword(keyword: str) -> None:
    """
    Validate search keyword is not empty.

    Args:
        keyword: Search keyword to validate

    Raises:
        TaskValidationError: If keyword is empty
    """
    if not keyword or not keyword.strip():
        raise TaskValidationError("Search keyword cannot be empty")