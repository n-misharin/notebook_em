import abc


class ValidateException(Exception):
    pass


class InputValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, data: str):
        pass


class StringValidator(InputValidator):
    """
    Base string validation class.
    """
    def __init__(self, min_length: int, max_length: int, alpha: set[str]):
        """
        :param min_length: int - min string length.
        :param max_length: int - max string length.
        :param alpha: set[str] - valid chars.
        """
        super().__init__()
        if min_length > max_length:
            raise ValueError("Invalid value: min_length > max_length.")
        self.max_length = max_length
        self.min_length = min_length
        self.alpha = alpha

    def validate(self, data: str):
        """
        Validate string.
        :param data: str
        :return:
        """
        if self.min_length > len(data) or len(data) > self.max_length:
            raise ValidateException(f"Invalid length. Length must be in [{self.min_length}, {self.max_length}].")

        for c in data:
            if c not in self.alpha:
                raise ValidateException(f"Invalid symbol `{c}`.")
