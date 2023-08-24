from functools import wraps

from notebook.settings import Settings


class CommandNameError(Exception):
    pass


class CommandContainer:
    """
    Container for commands.

    Attrs:
    -----
    commands: dict
        commands container.

    Methods:
    -----
    call(name: str, settings: Settings, *args, **kwargs) ->
    """

    def __init__(self) -> None:
        self.commands = dict()

    def call(self, name: str, settings: Settings, *args, **kwargs) -> object:
        """
        Call container command by string name.
        :param name: str - command name.
        :param settings: Settings - application settings.
        :param args: call function args.
        :param kwargs: call function kwargs
        :return:
        """
        if name not in self.commands.keys():
            raise CommandNameError(f"Command `{name}` not found.")
        return self.commands[name](settings, *args, **kwargs)

    def add(self, names: list[str], func: callable) -> None:
        """
        Add new command to container.
        :param names: list[str] - console command names.
        :param func: callable - command implementation function.
        :return:
        """
        for name in names:
            if name in self.commands.keys():
                raise CommandNameError(f"Command `{name}` already exist.")
            self.commands[name] = func

    def new(self, names: list[str]) -> callable:
        """
        Decoration command function.
        :param names: list[str] - command names.
        :return:
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            self.add(names, wrapper)
            return self.commands[names[0]]

        return decorator
