from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import QuerySet

from django.shortcuts import get_object_or_404

from notes.models import Note
from notes_api import serializers, permissions, filters


class ListNoteAPIView(APIView):
    """вывод всех "разрешенных" объектов"""
    permission_classes = (IsAuthenticated, permissions.EditPublicNotePermission)
    filter_backends = [DjangoFilterBackend]
    filtertodo = filters.FilterToDoList

    def get(self, request: Request) -> Response:
        notes_list = Note.objects.all()
        serializer = serializers.NotesSerializer(instance=notes_list, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = serializers.NotesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OneNoteAPIView(APIView):
    """
    вывод одного "разрешенного" объекта, с возможностью удаления, изменения
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, pk) -> Response:
        queryset = get_object_or_404(Note, pk=pk)
        serializer = serializers.NotesSerializer(instance=queryset)
        return Response(serializer.data)

    def put(self, request: Request, pk) -> Response:
        note = get_object_or_404(Note, pk=pk)
        serializer = serializers.NotesSerializer(instance=note, data=request.data)
        if serializer.is_valid() and note.author == request.user:
            serializer.save(author=request.user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, pk) -> Response:
        return self.put(request, pk)

    def delete(self, request: Request, pk) -> Response:
        note = get_object_or_404(Note, pk=pk)
        serializer = serializers.NotesSerializer(instance=note, data=request.data)
        if serializer.is_valid() and note.author == request.user:
            serializer.save(author=request.user)
            note.delete()
            note.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class NotesListCreateAPIView(generics.ListCreateAPIView):
    """
    просмотр только записей автора
    """
    queryset = Note.objects.all()
    serializer_class = serializers.NotesSerializer
    permission_classes = (IsAuthenticated, permissions.EditNotePermission)

    filter_backends = [DjangoFilterBackend]
    filtertodo = filters.FilterToDoList

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user).order_by('-up_to', '-importance')

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PublicNotesListAPIView(generics.ListAPIView):
    """
    просмотр только публичных записей
    """
    queryset = Note.objects.all()
    serializer_class = serializers.NotesSerializer
    permission_classes = (IsAuthenticated, permissions.EditPublicNotePermission)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_public=True).order_by('-up_to', '-importance')


# class FilterToDoListAPIView(generics.ListAPIView):
#     queryset = Note.objects.all()
#     serializer_class = serializers.NotesSerializer
#     permission_classes = [IsAuthenticated]


    # def filter_queryset(self, queryset):
    #     query_params = serializers.QueryParamsNotesFilterImpSerializer(data=self.request.query_params)
    #     query_params.is_valid(raise_exception=True)
    #
    #     list_importance = query_params.data.get('importance')
    #
    #     if list_importance:
    #         queryset = queryset.filter(importance__inn=query_params.data['importance'])
    #     return queryset
    #     # is_public = self.request.query_params.get('is_public')
    #     # for i in queryset:






