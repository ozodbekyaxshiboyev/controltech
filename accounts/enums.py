from enum import Enum


class UserRoles(Enum):
    manager = 'manager'
    student = 'student'
    family = 'family'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)

