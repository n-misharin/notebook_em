import dataclasses


@dataclasses.dataclass
class User:
    name: str
    surname: str
    patronymic: str
    organization: str
    phone: str
    work_phone: str
    id: int = None

    def __str__(self):
        return "\t".join([
            str(self.id),
            self.name,
            self.surname,
            self.patronymic,
            self.organization,
            self.phone,
            self.work_phone
        ])
