def dict_remove_empty(data: dict):
    """Remove empty values from data.

    Args:
        data (dict): Data

    Returns:
        dict: Data without empty values

    """
    return dict(filter(lambda x: x[1] is not None and x[1] != "", data.items()))
