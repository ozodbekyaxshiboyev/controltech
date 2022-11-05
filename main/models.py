from django.db import models
from accounts.models import User
from .enums import Books
from .services import location_image, validate_image, custom_validator, translate
from django.core.exceptions import ValidationError
from accounts.enums import UserRoles


class Basemodel(models.Model):
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract=True


class Report(Basemodel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='report')
    book = models.CharField(max_length=20, choices=Books.choices(), verbose_name="Kitob: ")
    from_lesson = models.PositiveIntegerField(blank=True, null=True, verbose_name="Qaysi darsdan: ")
    to_lesson = models.PositiveIntegerField(blank=True, null=True, verbose_name="Qaysi darsgacha: ")
    count = models.PositiveIntegerField(verbose_name="Soni",blank=True,null=True)
    words = models.TextField(verbose_name='So`zlarni bo`sh joy bilan ajratib vergul ishlatmay kiriting')
    comment = models.TextField(max_length=100, verbose_name="Izoh uchun joy: ",blank=True,null=True)
    similarity = models.FloatField(default=0,blank=True,null=True)
    is_verifyed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.created_at}  {self.user.full_name}"




class ReportItem(Basemodel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name='reportuser')
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    word = models.CharField(max_length=100, blank=True, null=True, verbose_name="so`z")
    word_translation = models.CharField(max_length=100, blank=True, null=True, verbose_name="tarjimasi")


    def __str__(self):
        return f"{self.word} - {self.word_translation}"


class Task(Basemodel):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='task')
    for_all_students = models.BooleanField(blank=True, null=True, verbose_name="Hamma student uchunmi?")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,verbose_name="Bitta student uchun", related_name="for_user")
    text = models.TextField(verbose_name="Taskni matni")
    image = models.ImageField(upload_to='task_images', validators=[validate_image, custom_validator],
                              blank=True, null=True, verbose_name="Fotosurat (ixtiyoriy)")
    source_file = models.FileField(upload_to='task_files', blank=True, null=True, verbose_name="Fayl (ixtiyoriy)")

    def clean(self):
        if self.creator.role == UserRoles.student.value:
            raise ValidationError({'Eslatma!': ('Taskni faqat boshqaruvchilar yaratishi mumkin!')})
        if self.for_all_students and self.user:
            raise ValidationError({'Eslatma!': ('Yoki bitta studentni yoki hammasini belgilang!!')})

    def __str__(self):
        return f"{self.created_at} {self.creator.full_name} {self.text[:30]}"


class TaskResult(Basemodel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='taskresult')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taskresult')
    text = models.TextField(verbose_name="Javob yozing")


    def __str__(self):
        return f"{self.created_at} {self.text}"


class Chat(Basemodel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='chats')
    text = models.TextField(verbose_name="matn")
    source_file = models.FileField(upload_to='chat_files', blank=True, null=True, verbose_name="fayl")



    def __str__(self):
        return f"{self.created_at} {self.text}"


class Dayplan(Basemodel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='dayplan')
    text = models.TextField()

    def __str__(self):
        return f"{self.user.full_name}  {self.text}"

class Reachment(Basemodel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reachment')
    text = models.TextField()
    image = models.ImageField(upload_to='reach_images', validators=[validate_image, custom_validator],
                              blank=True, null=True, verbose_name="Fotosurat (ixtiyoriy)")


    def __str__(self):
        return f"{self.user.full_name}  {self.text[:30]}"








###################
###################
###################
###################
###################
#
# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     duration = models.PositiveIntegerField()
#
#     def __str__(self):
#         return self.name
#
#
#
# class CustomUser(models.Model):
#     phone_number = models.CharField(max_length=13)
#     profile_image=models.ImageField(upload_to='user_images',null=True,blank=True)
#     verify_code = models.CharField(max_length=100,null=True,blank=True)
#     course = models.ManyToManyField('Course',related_name='course',null=True,blank=True)
#     course_assestant = models.ManyToManyField('Course',related_name='course_assestant',null=True,blank=True)
#     user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
#
#     def __str__(self) -> str:
#         return str(self.user)
#
#
#
# class Lesson(models.Model):
#     course = models.ForeignKey('Course',on_delete=models.CASCADE,default=None)
#     name = models.CharField(max_length=100)
#     source_file = models.FileField(upload_to='lesson_files',null=True,blank=True)
#     video_file = models.FileField(upload_to='lesson_videos',null=True,blank=True)
#     others = models.CharField(max_length=512,null=True,blank=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Task(models.Model):
#     number = models.PositiveIntegerField()
#     description = models.TextField()
#     image = models.ImageField(upload_to='task_images',null=True,blank=True)
#     lesson = models.ForeignKey('Lesson',on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.number)
#
#
#
# class TextTask(models.Model):
#     user = models.ForeignKey('CustomUser',on_delete=models.CASCADE)
#     task = models.ForeignKey('Task',on_delete=models.CASCADE)
#     is_user = models.BooleanField(default=False)
#     source_file = models.FileField(upload_to='texttask_files', null=True, blank=True)
#     source_text = models.CharField(max_length=512, null=True, blank=True)
#     send_time = models.DateTimeField(auto_now_add=True)
#
#
#
# class TextLesson(models.Model):
#     user = models.ForeignKey('CustomUser',on_delete=models.CASCADE)
#     lesson = models.ForeignKey('Lesson',on_delete=models.CASCADE)
#     is_user = models.BooleanField(default=False)
#     source_file = models.FileField(upload_to='textlesson_files', null=True, blank=True)
#     source_text = models.CharField(max_length=512)
#     send_time = models.DateTimeField(auto_now_add=True)





