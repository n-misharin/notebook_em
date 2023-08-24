import os
from typing import Iterator, Callable

from notebook.database.base import Table
from notebook.database.models import User


class UserTable(Table):
    # TODO: docs
    def __init__(self, filename: str, encoding="utf-8") -> None:
        self.encoding = encoding
        self._filename = filename
        self._last = 0
        self._create_copy()

    def append_row(self, user: User) -> User:
        with open(self._filename, mode="a", encoding=self.encoding) as file, \
                open(self._copy_filename(), mode="a", encoding=self.encoding) as copy_file:
            user.id = self._last + 1
            line = UserTable._to_line(user)
            file.write(line + "\n")
            copy_file.write(line + "\n")
            self._last += 1
        return user

    def update_row(self, row_number: int, new_data: User) -> User:
        with open(self._copy_filename(), mode="r", encoding=self.encoding) as copy_file, \
                open(self._filename, mode="w", encoding=self.encoding) as file:
            new_line = UserTable._to_line(new_data)
            for i, line in enumerate(copy_file):
                if i == row_number:
                    file.write(new_line + "\n")
                else:
                    file.write(line)
        self._create_copy()
        return new_data

    def insert_row(self, row_number: int, insert_data: User) -> User:
        with open(self._copy_filename(), mode="r", encoding=self.encoding) as copy_file, \
                open(self._filename, mode="w", encoding=self.encoding) as file:
            for i, line in enumerate(copy_file):
                if i == row_number:
                    new_line = UserTable._to_line(insert_data)
                    file.write(new_line + "\n")
                file.write(line)
        self._create_copy()
        return insert_data

    def get_row(self, user_id: int) -> User:
        with open(self._filename, mode="r", encoding=self.encoding) as file:
            for i, line in enumerate(file):
                user = self._to_object(line)
                if user.id == user_id:
                    return user
        raise IndexError(f"Line number out of range: expected < {i + 1}, but found {user_id}")

    def find(self, find_data: dict, comp: Callable[[dict, User], bool]) -> Iterator[User]:
        with open(self._filename, mode="r", encoding=self.encoding) as file:
            for line in file:
                user = self._to_object(line.strip())
                if comp(find_data, user):
                    yield user

    def delete_row(self, user_id: int) -> None:
        with open(self._filename, mode="w", encoding=self.encoding) as file, \
                open(self._copy_filename(), mode="r", encoding=self.encoding) as copy_file:
            for i, line in enumerate(copy_file):
                user = self._to_object(line)
                if user.id != user_id:
                    file.write(line)
        self._create_copy()

    def get_page(self, offset: int, limit: int) -> list[User]:
        res = []
        with open(self._filename, mode="r", encoding=self.encoding) as file:
            for i, line in enumerate(file):
                if i < offset:
                    continue
                if i > offset + limit:
                    break
                res.append(self._to_object(line.strip()))
        return res

    def _copy_filename(self) -> str:
        path = self._filename.split('/')
        path[-1] = f".{path[-1]}"
        return f"{'/'.join(path)}"

    def _create_copy(self) -> None:
        with open(self._filename, mode="r", encoding=self.encoding) as file, \
                open(self._copy_filename(), mode="w", encoding=self.encoding) as copy_file:
            for i, line in enumerate(file):
                copy_file.write(line)
                self._last = self._to_object(line).id

    def delete_copy(self) -> None:
        os.remove(self._copy_filename())

    @staticmethod
    def _to_line(data: User) -> str:
        return data.__str__().strip()

    @staticmethod
    def _to_object(data: str) -> User:
        user_id, *args = data.split("\t")
        return User(*args, id=int(user_id))
