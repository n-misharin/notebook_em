from notebook.database.models import User


def user_comparator(user_data: dict, user: User) -> bool:
    columns = []
    for key, value in user_data.items():
        if value is None or value == "" or key not in user.__dict__.keys():
            continue
        if key == "id":
            return value == user.id
        is_substring = value in user.__dict__.get(key, "")
        columns.append(is_substring)
    return all(columns)
