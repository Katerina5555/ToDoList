from django_filters import rest_framework as filters

from notes.models import Note
from notes_api import serializers


class FilterToDoList(filters.FilterSet):
    class Meta:
        model = Note
        fields = ['importance', 'is_public', 'status']

