class NotFoundInDatabaseException(Exception):
    """Exception raised when not found object in database.

    Attributes:
        message (str): explanation of the error

    """

    def __init__(self, table_name: str, keys: list[dict]):
        """Initialize the exception.

        Args:
            extension (str): extension of file
            search_key (str): search keys in database

        """

        self.message = f"Not found in table `{table_name}`: used keys -> {keys}."
        super().__init__(self.message)


class SoftDeleteDoesNotSupported(Exception):
    """Exception raised when object does not support soft delete.

    Attributes:
        message (str): explanation of the error

    """

    def __init__(self, model_name: str):
        """Initialize the exception.

        Args:
            model_name (str): name of model

        """

        self.message = f"Model {model_name} does not support soft delete"
        super().__init__(self.message)
