# Generated by Django 4.1.2 on 2022-11-02 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_for_user_task_user_remove_task_for_students_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='comment',
            field=models.TextField(help_text='Izoh uchun joy: ', max_length=200),
        ),
    ]