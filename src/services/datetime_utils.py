"""
Datetime utilities for the advanced todo CLI application.

This module provides utilities for time zone handling and date calculations.
"""

from datetime import datetime, timedelta
from typing import Optional


def get_current_datetime() -> datetime:
    """
    Get the current datetime in the system's local timezone.

    Returns:
        datetime: Current datetime in local timezone
    """
    return datetime.now()


def parse_datetime_string(datetime_str: str) -> Optional[datetime]:
    """
    Parse a datetime string into a datetime object.

    Supports formats:
    - YYYY-MM-DD
    - YYYY-MM-DD HH:MM
    - HH:MM (assumes today's date)

    Args:
        datetime_str: String representation of datetime

    Returns:
        datetime: Parsed datetime object or None if parsing fails
    """
    if not datetime_str:
        return None

    try:
        # Try YYYY-MM-DD HH:MM format first
        if " " in datetime_str and ":" in datetime_str:
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        # Try YYYY-MM-DD format
        elif "-" in datetime_str and len(datetime_str.split("-")[0]) == 4:
            date_part = datetime.strptime(datetime_str, "%Y-%m-%d").date()
            return datetime.combine(date_part, datetime.min.time())
        # Try HH:MM format (assumes today)
        elif ":" in datetime_str and len(datetime_str.split(":")) == 2:
            time_parts = datetime_str.split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            today = datetime.now().date()
            return datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
    except ValueError:
        pass

    return None


def is_datetime_in_future(dt: datetime) -> bool:
    """
    Check if a datetime is in the future compared to current time.

    Args:
        dt: DateTime to check

    Returns:
        bool: True if datetime is in the future, False otherwise
    """
    return dt > get_current_datetime()


def add_days(dt: datetime, days: int) -> datetime:
    """
    Add days to a datetime.

    Args:
        dt: Original datetime
        days: Number of days to add (can be negative)

    Returns:
        datetime: New datetime with days added
    """
    return dt + timedelta(days=days)


def add_weeks(dt: datetime, weeks: int) -> datetime:
    """
    Add weeks to a datetime.

    Args:
        dt: Original datetime
        weeks: Number of weeks to add (can be negative)

    Returns:
        datetime: New datetime with weeks added
    """
    return dt + timedelta(weeks=weeks)


def get_next_weekday(dt: datetime, target_weekday: int) -> datetime:
    """
    Get the next occurrence of a specific weekday.

    Args:
        dt: Starting datetime
        target_weekday: Target weekday (0=Monday, 6=Sunday)

    Returns:
        datetime: Next occurrence of the target weekday
    """
    days_ahead = target_weekday - dt.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return dt + timedelta(days_ahead)


def get_next_occurrence(dt: datetime, days_of_week: list) -> datetime:
    """
    Get the next occurrence based on days of the week.

    Args:
        dt: Starting datetime
        days_of_week: List of weekdays (0=Monday, 6=Sunday)

    Returns:
        datetime: Next occurrence based on days of week
    """
    if not days_of_week:
        return dt

    # Sort the days of week to ensure consistent behavior
    days_of_week = sorted(set(days_of_week))

    current_weekday = dt.weekday()

    # Find the next day in the list
    for day in days_of_week:
        if day > current_weekday:
            # Target day is later this week
            days_ahead = day - current_weekday
            return dt + timedelta(days=days_ahead)

    # If no day later in the week, use the first day of next week
    days_ahead = 7 - current_weekday + days_of_week[0]
    return dt + timedelta(days=days_ahead)