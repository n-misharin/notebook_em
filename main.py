from interface.commands.commands import commander
from notebook.database.table import UserTable
from notebook.notebook import NotebookApp

DATA_FILENAME = "data/db"

if __name__ == '__main__':
    app = NotebookApp(UserTable(DATA_FILENAME))
    app.register_commander(commander)
    app.start()
