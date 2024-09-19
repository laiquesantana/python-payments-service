import json

import aiofiles

from app.events import publisher


async def load_file_as_json(filepath):
    """Function to read json files from tests.

    Args:
    -   filepath(`str`) - Relative path to json file

    Returns:
    -    `dict` - Dict with json file content

    """
    fullpath = f"tests/resources/{filepath}"
    async with aiofiles.open(fullpath, "r") as f:
        json_string = await f.read()

    return json.loads(json_string)


def auth_header():
    """Auxiliar function with default auth header from tests.

    Returns:
    -   `dict` - Dict with auth header

    """
    return {"X-API-KEY": "test-api-key"}


# def get_published(key: str) -> list:
#     """Auxiliar function to get message from publisher mock.

#     Args:
#     -   key(`str`) - Key to search message

#     Return:
#     -   dict[str, Any] - Return the messages from key

#     """
#     return publisher.CALLS[key]


def params_to_string(params: dict) -> str:
    """Aux function to conv dict params to string url.

    Args:
    -   params(`dict`): Dict with url params

    Returns:
    -   params_text(`str`): Formatted string with url params

    """
    params_formatted = []
    for key, value in params.items():
        params_formatted.append(f"{key}={value}")

    return "&".join(params_formatted)
