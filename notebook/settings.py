import dataclasses

from notebook.database.table import UserTable


@dataclasses.dataclass
class Settings:
    database: UserTable
    running: bool = False
