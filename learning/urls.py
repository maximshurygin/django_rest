from django.urls import path

from learning.apps import LearningConfig
from rest_framework.routers import DefaultRouter

from learning.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentsListAPIView, subscribe, unsubscribe, create_payment, \
    retrieve_payment

app_name = LearningConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
                  path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
                  path('subscribe/<int:course_id>/', subscribe, name='subscribe'),
                  path('unsubscribe/<int:course_id>/', unsubscribe, name='unsubscribe'),
                  path('create-payment/', create_payment, name='create-payment'),
                  path('retrieve-payment/<str:payment_intent_id>/', retrieve_payment, name='retrieve-payment'),
              ] + router.urls
