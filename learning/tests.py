from rest_framework import status
from rest_framework.test import APITestCase

from learning.models import Lesson, Course, Subscription

from users.models import User


class LearningTestCase1(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            'title': 'Test',
            'description': 'Test',
            'video_url': 'https://youtube.com/test'
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'Test', 'description': 'Test', 'image': None,
             'video_url': 'https://youtube.com/test', 'course': None, 'owner': 1}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """Тестирование отображения списка уроков"""

        Lesson.objects.create(
            title='list test',
            description='test',
            video_url='https://youtube.com/test'
        )

        response = self.client.get(
            '/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        expected_response = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 2,
                    'title': 'list test',
                    'description': 'test',
                    'image': None,
                    'video_url': 'https://youtube.com/test',
                    'course': None,
                    'owner': None
                }
            ]
        }
        self.assertEqual(response.json(), expected_response)

    def test_retrieve_lesson(self):
        """Тестирование отображения урока"""
        Lesson.objects.create(
            title='detail test',
            description='test',
            video_url='https://youtube.com/test',
            owner=self.user
        )

        response = self.client.get(
            '/lesson/3/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        lesson = Lesson.objects.create(
            title='old test',
            description='test',
            video_url='https://youtube.com/test',
            owner=self.user
        )

        response = self.client.patch(
            f'/lesson/update/{lesson.pk}/',
            {'title': 'new test'}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class LearningTestCase2(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        lesson = Lesson.objects.create(
            title='delete test',
            description='test',
            video_url='https://youtube.com/test',
            owner=self.user
        )

        response = self.client.delete(
            f'/lesson/delete/{lesson.pk}/'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=lesson.pk).exists())


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpass')
        self.course = Course.objects.create(
            title='Test Course',
            description='test'
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        """Тестирование подписки"""
        response = self.client.post(f'/subscribe/{self.course.id}/')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe(self):
        """Тестирование отписки"""
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete(f'/unsubscribe/{self.course.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
