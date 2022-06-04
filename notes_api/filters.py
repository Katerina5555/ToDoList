from django_filters import rest_framework as filters

from notes.models import Note


class FilterToDoList(filters.FilterSet):
    class Meta:
        model = Note
        fields = ['importance',
                'is_public',
                'status']
