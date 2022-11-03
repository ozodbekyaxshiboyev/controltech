from django.core.exceptions import ValidationError


def location_image(instance, file):
    return f'users/{instance.role}/{instance.firstname}_{file}'

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Fotosurat o`lchami uzog`i bilan %sMBgacha" % str(megabyte_limit))

def custom_validator(value):
    valid_formats = ['png', 'jpeg', 'jpg', 'vsg']
    if not any([True if value.name.lower().endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{value.name} noaniq formatli surat')