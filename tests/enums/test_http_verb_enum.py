import pytest

from app.enums import HTTPVerbs


@pytest.mark.parametrize(
    "value",
    [
        "get",
        "post",
        "put",
        "delete",
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ],
)
async def test_has_value(value: str):
    """Test method has_value from enum class HTTPVerbs.

    Args:
    -   value(`str`): Value to check

    """
    # Assert
    assert HTTPVerbs.has_value(value)


@pytest.mark.parametrize(
    "value",
    [
        "PATCH",
        "OPTIONS",
    ],
)
async def test_has_value_unknown(value: str):
    """Test exception in has_value from enum class HTTPVerbs.

    Args:
    -   value(`str`): Value unknown

    """
    # Act  / Assert
    assert HTTPVerbs.has_value(value) is False


@pytest.mark.parametrize(
    "value,valued_expected",
    [
        ("get", "GET"),
        ("post", "POST"),
        ("put", "PUT"),
        ("delete", "DELETE"),
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
    ],
)
async def test_get_value(value: str, valued_expected: str):
    """Test successfully get_value from enum class HTTPVerbs.

    Args:
    -   value(`str`): Value to get
    -   valued_expected(`str`): Value expected

    """
    # Act
    value = HTTPVerbs.get_value(value)

    # Assert
    assert value == valued_expected


@pytest.mark.parametrize(
    "value",
    [
        "PATCH",
        "OPTIONS",
    ],
)
async def test_get_value_unknown(value: str):
    """Test exception in get_value from enum class HTTPVerbs.

    Args:
    -   value(`str`): Value unknown

    """
    message_expected = f"Unknown HTPP verb: `{value}`"

    # Act  / Assert
    with pytest.raises(ValueError, match=message_expected):
        HTTPVerbs.get_value(value)
