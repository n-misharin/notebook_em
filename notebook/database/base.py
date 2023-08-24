import abc
from typing import TypeVar, Generic, Callable, Iterator

T = TypeVar("T")


class Table(abc.ABC, Generic[T]):
    """
    Abstract table class.

    Attrs:
    -----
    encoding: str
        file encoding
    _filename: str
        table path to file and file name

    Methods:
    -----
    delete_row(row_number: int) -> None:
        delete row from file by row number
    append_row(append_data: T) -> T:
        append row to file
    update_row(row_number: int, new_data: T) -> T:
        edit row in table

    """

    # TODO: docs

    @abc.abstractmethod
    def delete_row(self, row_number: int) -> None:
        pass

    @abc.abstractmethod
    def append_row(self, append_data: T) -> T:
        pass

    @abc.abstractmethod
    def update_row(self, row_number: int, new_data: T) -> T:
        pass

    @abc.abstractmethod
    def insert_row(self, row_number: int, insert_data: T) -> T:
        pass

    @abc.abstractmethod
    def get_row(self, row_number: int) -> T:
        pass

    @abc.abstractmethod
    def get_page(self, offset: int, limit: int) -> T:
        pass

    @abc.abstractmethod
    def find(self, find_data: dict, comp: Callable[[T], bool]) -> Iterator[T]:
        pass
