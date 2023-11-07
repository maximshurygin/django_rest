from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config import settings
from learning.models import Course, Lesson, Payments, Subscription
from learning.paginators import LearningPaginator
from learning.permissions import IsNotModerator, IsOwnerOrModerator, CustomViewSetPermissions
from learning.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer
import stripe
from stripe.error import StripeError

stripe.api_key = settings.STRIPE_SECRET_KEY


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, CustomViewSetPermissions]
    pagination_class = LearningPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Course.objects.all().order_by('id')


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = LearningPaginator

    def get_queryset(self):
        return Lesson.objects.all().order_by('id')


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator, IsOwnerOrModerator]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)
    if created:
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unsubscribe(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    subscription = get_object_or_404(Subscription, user=request.user, course=course)
    subscription.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def create_payment(request):
    try:
        amount = 1000
        currency = 'usd'
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['card'],
        )
        return JsonResponse({'clientSecret': payment_intent['client_secret']})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)


def retrieve_payment(request, payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return JsonResponse(payment_intent)
    except StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)
