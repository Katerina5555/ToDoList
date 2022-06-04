from rest_framework import serializers
from datetime import datetime

from notes.models import Note


class NotesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Note
        fields = "__all__"

    # def to_representation(self, instance):
    #     """
    #     переопределение вывода даты (С ПРАКТИКИ). Для разбора
    #     """
    #     ret = super().to_representation(instance)
    #     create_at = datetime.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    #     try:
    #         update_at = datetime.strptime(ret['up_to'], '%Y-%m-%dT%H:%M:%SZ')
    #     except:
    #         update_at = datetime.strptime(ret['up_to'], '%Y-%m-%dT%H:%M:%S.%fZ')
    #     ret['create_at'] = create_at.strftime('%d %B %Y %H:%M:%S')
    #     ret['up_to'] = update_at.strftime('%d %B %Y %H:%M:%S')
    #     return ret


# Попробовать вывести фильтры таки образом. Не загружен
# class QueryParamsNotesFilterImpSerializer(serializers.Serializer):
#     importance = serializers.ListField(child=serializers.BooleanField,
#                                        required=False)
#
#
# class QueryParamsNotesFilterPubSerializer(serializers.Serializer):
#     is_public = serializers.ListField(child=serializers.BooleanField,
#                                       required=False)
#
#
# class QueryParamsNotesFilterStatSerializer(serializers.Serializer):
#     status = serializers.ListField(child=serializers.ChoiceField(choices=Note.status.numerator),
#                                    required=False)

