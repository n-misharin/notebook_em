import string
from typing import Optional

import phonenumbers

from interface.utils.validators import InputValidator, StringValidator, ValidateException
from notebook.database.models import User

MIN_NAME_LEN = 1
MAX_NAME_LEN = 50

MIN_ORGANIZATION_NAME_LEN = 2
MAX_ORGANIZATION_NAME_LEN = 150

NAME_ALPHA = {
    *list(string.ascii_letters),
    " ", '"', "'"
}
ORGANIZATION_ALPHA = {
    *NAME_ALPHA,
    *list(string.digits)
}


class IdValidator(InputValidator):
    def validate(self, data: str):
        try:
            data = int(data)
        except ValueError:
            raise ValidateException("Value must be `int`.")

        if data < 0:
            raise ValidateException("Value must be non negative.")


class NameValidator(StringValidator):
    def __init__(self):
        super().__init__(MIN_NAME_LEN, MAX_NAME_LEN, NAME_ALPHA)


class OrganizationNameValidator(StringValidator):
    def __init__(self):
        super().__init__(MIN_ORGANIZATION_NAME_LEN, MAX_ORGANIZATION_NAME_LEN, ORGANIZATION_ALPHA)


class PhoneNumberValidator(InputValidator):
    def validate(self, data: str):
        try:
            phone = phonenumbers.parse(data)
        except Exception:
            raise ValidateException("Invalid phone number.")

        if not phonenumbers.is_valid_number(phone):
            raise ValidateException("Invalid phone number.")


def read_line_while_not_valid(
        message: str,
        validator: InputValidator,
        stop_value: str = None,
        default_value: str = None
) -> Optional[str]:
    while True:
        data = input(f"{message}: ")
        if data == stop_value:
            return default_value
        try:
            validator.validate(data)
            return data
        except ValidateException as e:
            print(e)


def read_user() -> User:
    name_validator = NameValidator()
    name = read_line_while_not_valid("enter name", name_validator)
    surname = read_line_while_not_valid("enter surname", name_validator)
    patronymic = read_line_while_not_valid("enter patronymic", name_validator)

    organization = read_line_while_not_valid("enter organization", OrganizationNameValidator())

    phone_validator = PhoneNumberValidator()
    phone = read_line_while_not_valid("enter personal phone", phone_validator)
    work_phone = read_line_while_not_valid("enter work phone", phone_validator)

    return User(name, surname, patronymic, organization, phone, work_phone)


def update_user(user: User) -> User:
    message = "Enter a new `{}` value or press `enter` to leave  the old one [{}]"
    name = read_line_while_not_valid(
        message.format("name", user.name),
        NameValidator(),
        stop_value="",
        default_value=user.name
    )
    surname = read_line_while_not_valid(
        message.format("surname", user.surname),
        NameValidator(),
        stop_value="",
        default_value=user.surname
    )
    patronymic = read_line_while_not_valid(
        message.format("patronymic", user.patronymic),
        NameValidator(),
        stop_value="",
        default_value=user.patronymic
    )
    organization = read_line_while_not_valid(
        message.format("organization", user.organization),
        OrganizationNameValidator(),
        stop_value="",
        default_value=user.organization
    )
    phone = read_line_while_not_valid(
        message.format("phone", user.phone),
        PhoneNumberValidator(),
        stop_value="",
        default_value=user.phone
    )
    work_phone = read_line_while_not_valid(
        message.format("work phone", user.work_phone),
        PhoneNumberValidator(),
        stop_value="",
        default_value=user.work_phone
    )
    return User(name, surname, patronymic, organization, phone, work_phone, id=user.id)


def find() -> dict:
    user_id = read_line_while_not_valid("enter user id", IdValidator(), stop_value="", default_value=None)
    if user_id is not None:
        return {
            "id": int(user_id)
        }

    name_validator = NameValidator()
    res = dict()

    res["name"] = read_line_while_not_valid(
        "enter name",
        name_validator,
        stop_value="",
        default_value=None
    )
    res["surname"] = read_line_while_not_valid(
        "enter surname",
        name_validator,
        stop_value="",
        default_value=None
    )
    res["patronymic"] = read_line_while_not_valid(
        "enter patronymic",
        name_validator,
        stop_value="",
        default_value=None
    )
    res["organization"] = read_line_while_not_valid(
        "enter organization",
        OrganizationNameValidator(),
        stop_value="",
        default_value=None
    )

    phone_validator = PhoneNumberValidator()
    res["phone"] = read_line_while_not_valid(
        "enter personal phone",
        phone_validator,
        stop_value="",
        default_value=None
    )
    res["work_phone"] = read_line_while_not_valid(
        "enter work phone",
        phone_validator,
        stop_value="",
        default_value=None
    )

    return {
        key: value
        for key, value in res.items() if value is not None
    }


def delete_user() -> Optional[str]:
    return read_line_while_not_valid(
        "enter user id",
        IdValidator(),
        stop_value="",
        default_value=None
    )

