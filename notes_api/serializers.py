from rest_framework import serializers

from notes.models import Note


class NotesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Note
        fields = "__all__"


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

