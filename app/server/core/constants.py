"""
Configuration constants for the Natural Language SQL Interface.

This module contains shared constants used across the application,
particularly for handling nested data structures in file uploads.

Constants:
    NESTED_FIELD_DELIMITER: The delimiter used to concatenate nested field names
                           when flattening JSON/JSONL objects. For example, a nested
                           structure like {"user": {"address": {"city": "NYC"}}} becomes
                           a flat field "user__address__city".

    LIST_INDEX_DELIMITER: The delimiter used to denote list item indices when
                         flattening arrays. For example, an array ["a", "b", "c"]
                         becomes fields "array_0", "array_1", "array_2".

Example:
    >>> from core.constants import NESTED_FIELD_DELIMITER, LIST_INDEX_DELIMITER
    >>> nested_field = f"user{NESTED_FIELD_DELIMITER}address{NESTED_FIELD_DELIMITER}city"
    >>> print(nested_field)
    'user__address__city'
    >>> list_field = f"tags{LIST_INDEX_DELIMITER}0"
    >>> print(list_field)
    'tags_0'
"""

# Delimiter for concatenating nested field names
# Example: {"user": {"name": "John"}} -> "user__name"
NESTED_FIELD_DELIMITER = "__"

# Delimiter for denoting list item indices
# Example: {"tags": ["python", "sql"]} -> "tags_0", "tags_1"
LIST_INDEX_DELIMITER = "_"
