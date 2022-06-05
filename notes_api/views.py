import self as self
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from django.db.models import QuerySet

from django.shortcuts import get_object_or_404

from notes.models import Note
from notes_api import serializers, permissions, filters


# def _check_permission_auth(request: Request, pk):
#     note = get_object_or_404(Note, pk=pk)
#     serializer = serializers.NotesSerializer(instance=note, data=request.data)
#     if note.author != request.user:
#         return Response(serializer.data, status.HTTP_403_FORBIDDEN)
#     return Response(serializer.data)
#
#
# def _check_permission_public(request: Request, pk):
#     note = get_object_or_404(Note, pk=pk)
#     serializer = serializers.NotesSerializer(instance=note, data=request.data)
#     if note.is_public != 1:
#         return Response(status.HTTP_404_NOT_FOUND)
#     return Response(serializer.data)


class ListNoteAPIView(APIView):
    """Выводятся все объекты.
    Просматривать их может только approved_user (задается в классе)"""
    _approved_user = 'admin'

    def get(self, request: Request) -> Response:
        if str(request.user) == ListNoteAPIView._approved_user:
            notes_list = Note.objects.all()
            serializer = serializers.NotesSerializer(instance=notes_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(f'Текущий пользователь: {str(request.user)}. '
                            f'Просмотр возможен только пользователем {ListNoteAPIView._approved_user}'
                            , status=status.HTTP_403_FORBIDDEN)

    def post(self, request: Request) -> Response:
        serializer = serializers.NotesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OneNoteAPIView(APIView):
    """
    Осуществляется вывод объекта по ключу, проводится проверка на авторство,
    если не автор - проверка на публичность. Читать непубличные записи другого пользователя нельзя.
    Удалять записи другого пользователя нельзя (несмотря на публичность)
    """
    permission_classes = (IsAuthenticated, permissions.EditNotePermission)

    def get(self, request: Request, pk) -> Response:
        queryset = get_object_or_404(Note, pk=pk)
        serializer = serializers.NotesSerializer(instance=queryset)
        if queryset.author != request.user:
            if queryset.is_public != 1:
                return Response(status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        return self.partial_change(request, pk=pk, partial=False)

    def partial_change(self, request:Request, pk: int, partial: bool) -> Response:
        """Выполнение частичного или полного обновления полей"""
        instance = get_object_or_404(Note, pk=pk)
        serializer = serializers.NotesSerializer(instance=instance, data=self.request.data, partial=partial)
        if serializer.is_valid(True) and instance.author == request.user:
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_403_FORBIDDEN)

    def patch(self, request: Request, pk) -> Response:
        return self.partial_change(request, pk=pk, partial=True)

    def delete(self, request: Request, pk):
        queryset = get_object_or_404(Note, pk=pk)
        if queryset.author == request.user:
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class NotesListCreateAPIView(generics.ListCreateAPIView):
    """
    Просмотр всех записей автора
    """
    queryset = Note.objects.all()
    serializer_class = serializers.NotesSerializer
    permission_classes = (IsAuthenticated, permissions.EditNotePermission)

    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.FilterToDoList

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user).order_by('-up_to', '-importance')

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PublicNotesListAPIView(generics.ListAPIView):
    """
    Просмотр только публичных записей
    """
    queryset = Note.objects.all()
    serializer_class = serializers.NotesSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_public=True).order_by('-up_to', '-importance')


class FilterToDoListAPIView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NotesSerializer

    def filter_queryset_importance(self, queryset):
        query_params = serializers.QueryParamsNotesFilterImpSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)

        list_importance = query_params.data.get('importance')
        if list_importance:
            queryset = queryset.filter(importance__in=query_params.data['importance'])
        return queryset

    def filter_queryset_public(self, queryset):
        query_params = serializers.QueryParamsNotesFilterPubSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)
        list_public = query_params.data.get('is_public')
        if list_public:
            queryset = queryset.filter(importance__in=query_params.data['is_public'])
        return queryset

    def filter_queryset_status(self, queryset):
        query_params = serializers.QueryParamsNotesFilterStatSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)
        list_status = query_params.data.get('status')
        if list_status:
            queryset = queryset.filter(importance__in=query_params.data['status'])
        return queryset











