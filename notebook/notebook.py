from typing import Type

from notebook.command_container import CommandContainer
from notebook.database.table import UserTable
from notebook.parser import Parser
from notebook.settings import Settings


class NotebookApp:
    """
    Notebook application class.

    Attrs:
    -----
    settings: Settings
        application settings
    commander: CommandContainer
        container for console commands
    command_parser: Type[Parser]
        console command parser class

    Methods:
    -----
    register_commander(commander: CommandContainer) -> None:
        register console commands
    start() -> None:
        start `notebook` application
    """
    def __init__(self, database: UserTable, command_parser: Type[Parser] = Parser) -> None:
        """
        Create application.
        :param database: DBHelper.
        :param command_parser: Parser class.
        """
        self.settings = Settings(database)
        self.commander = CommandContainer()
        self.commander.add(["help"], self._help)
        self.command_parser = command_parser

    def register_commander(self, commander: CommandContainer) -> None:
        """
        Register console commands.
        :param commander: CommandContainer with console commands.
        :return:
        """
        for key, val in commander.commands.items():
            self.commander.add([key], val)

    def start(self) -> None:
        """
        Start application. After the start, the application will accept console commands
        that are in `self.commander`.
        :return:
        """
        self.settings.running = True
        print("App is running.")
        print("Enter `help` to call help.")
        while self.settings.running:
            try:
                command_name, *args = self.command_parser.parse(input())
                self.commander.call(command_name, self.settings, *args)
            except Exception as e:
                print("\033[91mError:", e, "\033[0m")

    def _help(self, settings: Settings) -> None:
        """
        Print help.
        :param settings: App settings.
        :return:
        """
        print_commands = dict()
        for key, value in self.commander.commands.items():
            if value not in print_commands.keys():
                print_commands[value] = []
            print_commands[value].append(key)

        for key, value in print_commands.items():
            lines = []
            if isinstance(key.__doc__, str):
                for line in key.__doc__.split("\n"):
                    if ":param settings:" in line or ":return:" in line:
                        continue
                    lines.append("\t" + line.strip())
            print(", ".join(value), "\n".join(lines))
