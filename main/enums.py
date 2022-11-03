from enum import Enum


class Books(Enum):
    one = '1'
    two = '2'
    three = '3'
    four = '4'
    five = '5'
    sex = '6'
    other = 'other'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)

