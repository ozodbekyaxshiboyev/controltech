# Generated by Django 4.1.2 on 2022-11-04 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_alter_chat_created_at_alter_dayplan_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportitem',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='reportitem',
            name='image',
        ),
        migrations.AddField(
            model_name='report',
            name='words',
            field=models.TextField(default=11, verbose_name='So`zlarni bo`sh joy bilan ajratib vergul ishlatmay kiriting'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reportuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='word',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='so`z'),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='word_translation',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='tarjimasi'),
        ),
        migrations.AlterField(
            model_name='report',
            name='comment',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Izoh uchun joy: '),
        ),
        migrations.AlterField(
            model_name='report',
            name='count',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Soni'),
        ),
    ]