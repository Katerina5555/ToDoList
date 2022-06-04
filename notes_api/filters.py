from django_filters import rest_framework as filters

from notes.models import Note
from notes_api import serializers


class FilterToDoList(filters.FilterSet):
    class Meta:
        model = Note
        fields = ['importance',
                'is_public',
                'status']


def filter_queryset(self, queryset):
    query_params = serializers.QueryParamsNotesFilterImpSerializer(data=self.request.query_params)
    query_params.is_valid(raise_exception=True)
    return queryset


    #
    #     list_importance = query_params.data.get('importance')
    #
    #     if list_importance:
    #         queryset = queryset.filter(importance__inn=query_params.data['importance'])
    #     return queryset
    #     # is_public = self.request.query_params.get('is_public')
    #     # for i in queryset: