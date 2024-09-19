class IncompatibleFileExtensionException(Exception):
    """Exception raised when have incompatibility between extension and file
    content.

    Attributes:
        message (str): explanation of the error

    """

    def __init__(self, extension, mimetype):
        """Initialize the exception.

        Args:
            extension (str): extension of file
            mimetype (str): mimetype of file

        """

        self.message = (
            f"Incompatible file extension `{extension}` with mimetype `{mimetype}."
        )
        super().__init__(self.message)


class MaxFileSizeExceededException(ValueError):
    """Exception raised when file size exceed max size.

    Attributes:
        message (str): explanation of the error

    """

    def __init__(self, file_size, max_size):
        """Initialize the exception.

        Args:
            file_size (int): size of file
            max_size (int): max size of file

        """

        self.message = (
            f"File size `{file_size}` bytes exceed max size `{max_size} bytes."
        )
        super().__init__(self.message)
