from django.core.exceptions import ValidationError
from googletrans import Translator


def location_image(instance, file):
    return f'{instance.role}/{instance.firstname}_{file}'

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

def custom_validator(value):
    valid_formats = ['png', 'jpeg', 'jpg', 'vsg']
    if not any([True if value.name.lower().endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{value.name} is not a valid image format')


def translate(name):
    translator = Translator()
    lan = translator.detect(name).lang
    if lan == 'en':
        return translator.translate(name, src='en', dest='uz').text
    else:
        return translator.translate(name, dest='en').text
