from interface.utils.comparators import user_comparator
from interface.utils.inputs import read_user, update_user, find, delete_user
from notebook.command_container import CommandContainer
from notebook.settings import Settings

PAGE_SIZE = 10

commander = CommandContainer()


@commander.new(["quit", "q", "exit"])
def close_app(settings: Settings) -> None:
    """
    Stop application.
    :param settings: App settings.
    :return:
    """
    settings.running = False
    settings.database.delete_copy()
    print("Goodbye!")


@commander.new(["print", "write", "page", "p"])
def print_page(settings: Settings, page_number: int) -> None:
    """
    Printing page by page number.
    :param settings: App settings.
    :param page_number: int page number (numerated from 1).
    :return:
    """
    offset = (int(page_number) - 1) * PAGE_SIZE
    users = settings.database.get_page(offset, PAGE_SIZE)
    print("\n".join([str(user) for user in users]))


@commander.new(["add", "new", "a"])
def add_user(settings: Settings) -> None:
    """
    Add new user to notebook.
    :param settings: App settings.
    :return:
    """
    user_data = read_user()
    settings.database.append_row(user_data)


@commander.new(["edit", "update", "u"])
def update(settings: Settings, row_number: int) -> None:
    """
    Edit user data from the notebook.
    :param settings: App settings.
    :param row_number: int user id.
    :return:
    """
    row_number = int(row_number)
    old_user_data = settings.database.get_row(row_number)
    new_user_data = update_user(old_user_data)
    settings.database.update_row(row_number, new_user_data)


@commander.new(["search", "s", "find"])
def find_user(settings: Settings) -> None:
    """
    Find user by params.
    :param settings: Settings - app settings.
    :return:
    """
    user_data = find()
    print("find data:", user_data)
    print("result list:")
    for user in settings.database.find(user_data, user_comparator):
        print("\t", user)
    print("end list")


@commander.new(["delete", "d"])
def delete(settings: Settings):
    """
    Delte user from database.
    :param settings: Settings - app settings.
    :return:
    """
    user_id = delete_user()
    if user_id is not None:
        settings.database.delete_row(int(user_id))
