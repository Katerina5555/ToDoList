from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

from notes.models import Note


class TestListNoteAPIView(APITestCase):
    USER_1 = dict(
        username="username_1",
        password="fake_password",
    )

    @classmethod
    def setUpTestData(cls):
        """
        Создание пользователей.
        Внесение 2-х записей
        """
        # Добавление пользователя
        db_user_1 = User(**cls.USER_1)
        cls.db_user_1 = db_user_1
        db_user_1.save()

        # добавление записей
        notes = [
            Note(title="title_public_true", author=db_user_1, is_public=True),
            Note(title="title_public_false", author=db_user_1, is_public=False),
         ]
        Note.objects.bulk_create(notes)

    def test_list_objects_for_approved(self):
        """
        Проверка видимости всех записей (по умолчанию установлено, что всех видит Админ)
        :return: Запрос админа - выводятся все записи
        """
        url = "/api/v1/notes/"
        self.auth_admin = APIClient()
        self.auth_admin.force_authenticate(user="admin")
        resp = self.auth_admin.get(url)

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_list_objects_for_not_approved(self):
        """
        Проверка видимости всех записей (по умолчанию установлено, что всех видит Админ,
        остальные в данном запросе не видят ничего)
        :return:
        """
        url = "/api/v1/notes/"
        self.auth_user_1 = APIClient()
        self.auth_user_1.force_authenticate(user=self.db_user_1)
        resp = self.auth_user_1.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)


class TestOneNoteAPIView(APITestCase):
    USER_1 = dict(
        username="username_1",
        password="fake_password",
    )
    USER_2 = dict(
        username="user_2",
        password="fake_password",
    )

    @classmethod
    def setUpTestData(cls):
        """
        Создание пользователей.
        Внесение 3-х записей
        """

        # Добавление пользователей в БД
        db_user_1 = User(**cls.USER_1)
        cls.db_user_1 = db_user_1
        db_user_1.save()
        db_user_2 = User(**cls.USER_2)
        cls.db_user_2 = db_user_2
        db_user_2.save()

        # добавление записей
        notes = [
            Note(title="title_public_true", author=db_user_1, is_public=True),
            Note(title="title_public_false", author=db_user_2, is_public=False),
            Note(title="title_public_false", author=db_user_1, is_public=False),
            Note(title="title_public_false", author=db_user_2, is_public=True),
         ]
        Note.objects.bulk_create(notes)

    def setUp(self) -> None:
        """
        Согзание и авторизация нового клиента
        """
        self.auth_user_2 = APIClient()
        self.an_auth_user = APIClient()
        self.auth_user_2.force_authenticate(user=self.db_user_2)

    def test_get_not_public_for_author(self):
        """
        Проверка получения непубличной записи самим автором по id
        """
        note_pk = 2    # запись пользователя: user2, непубличная
        url = "/api/v1/note/"
        self.auth_user_2 = APIClient()
        self.auth_user_2.force_authenticate(user=self.db_user_2)
        resp = self.auth_user_2.get(url+str(note_pk))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_not_public_for_not_author(self):
        """
        Проверка получения непубличной записи другого автора по id
        """
        note_pk = 3  # # запись пользователя: user1, непубличная
        url = "/api/v1/note/"
        self.auth_user_2 = APIClient()
        self.auth_user_2.force_authenticate(user=self.db_user_2)
        resp = self.auth_user_2.get(url + str(note_pk))
        self.assertEqual(resp.data, status.HTTP_403_FORBIDDEN)

    def test_get_public_for_not_author(self):
        """
        Проверка получения публичной записи другого автора по id
        """
        note_pk = 1  # # запись пользователя: user1, публичная
        url = "/api/v1/note/"
        self.auth_user_2 = APIClient()
        self.auth_user_2.force_authenticate(user=self.db_user_2)
        resp = self.auth_user_2.get(url + str(note_pk))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_authors_note(self):
        """
        Проверка изменения своих записей по id
        """
        note_pk = 2  # # запись пользователя: user2, непубличная
        url = "/api/v1/note/"
        self.auth_user_2 = APIClient()
        self.auth_user_2.force_authenticate(user=self.db_user_2)
        resp = self.auth_user_2.patch(url + str(note_pk))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_not_authors_note(self):
        """
        Проверка изменения чужих записей по id
        """
        note_pk = 3  # запись пользователя: user1, непубличная
        url = "/api/v1/note/"
        self.auth_user_2 = APIClient()
        self.auth_user_2.force_authenticate(user=self.db_user_2)
        resp = self.auth_user_2.patch(url + str(note_pk))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_authors_note(self):
        """
        Проверка удаления своих записей по id
        """
        note_pk = 2  # запись пользователя: user2, непубличная
        url = "/api/v1/note/"
        self.auth_user_2 = APIClient()
        self.auth_user_2.force_authenticate(user=self.db_user_2)
        resp = self.auth_user_2.delete(url + str(note_pk))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_authors_note(self):
        """
        Проверка удаления чужих записей по id
        """
        note_pk = 3  # # запись пользователя: user1, непубличная
        url = "/api/v1/note/"
        self.auth_user_2 = APIClient()
        self.auth_user_2.force_authenticate(user=self.db_user_2)
        resp = self.auth_user_2.delete(url + str(note_pk))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)



# Вспомогательное для проверки резальтатов во время написания:
        # responce_data = resp.data
        # expected_data = []
        # self.assertEqual(expected_data, responce_data)
