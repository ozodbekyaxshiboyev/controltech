from enum import Enum


class UserRoles(Enum):
    maincontroller = 'maincontroller'
    controller = 'controller'
    student = 'student'
    family = 'family'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)

