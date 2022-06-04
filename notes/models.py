import datetime

from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


def for_date_plus_one():
    return datetime.datetime.now() + timedelta(days=1)


class Note(models.Model):

    class NoteStatus(models.IntegerChoices):
        POSTPONED = 0, _('Отложена')
        ACTIVE = 1, _('Активна')
        DONE = 2, _('Выполнена')

    title = models.CharField(max_length=50, verbose_name="Название заметки")
    note = models.TextField(default='', verbose_name='Описание')
    is_public = models.BooleanField(default=False, verbose_name='Публично')
    importance = models.BooleanField(default=False, verbose_name='Важность')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    up_to = models.DateTimeField(default=for_date_plus_one, verbose_name='Срок исполнения`')
    status = models.IntegerField(default=NoteStatus.ACTIVE, choices=NoteStatus.choices, verbose_name='Статус выполнения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
