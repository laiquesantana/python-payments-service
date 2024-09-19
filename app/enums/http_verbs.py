# This module defines an enumeration class `HTTPVerbs` that represents the standard HTTP verbs (GET, POST, PUT, DELETE).

# The `HTTPVerbs` class provides the following functionalities:
# - Enumerates the HTTP verbs as class attributes.
# - Provides a class method `has_value` to check if a given string is a valid HTTP verb.
# - Provides a class method `get_value` to return the formatted HTTP verb if it is valid, otherwise raises a `ValueError`.

# Usage:
# - This class can be used to validate and standardize HTTP verbs in an application, ensuring that only the defined verbs are used.
from enum import Enum


class HTTPVerbs(str, Enum):
    """Enumerate class to define accepted http verbs."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Check enum have a value.

        Args:
        -   value(`str`) : Searched value

        Returns:
        -   bool: Return True if have a value, false otherwise

        """
        return bool(value.upper() in cls._value2member_map_)

    @classmethod
    def get_value(cls, value: str) -> str:
        """Check enum have a value.

        Args:
        -   value(`str`) : Searched value

        Return:
        -   value(`str`) : Return formatted enum value

        """
        if not cls.has_value(value):
            raise ValueError(f"Unknown HTPP verb: `{value}`.")

        return value.upper()
