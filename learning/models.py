from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='course_images/', verbose_name='Превью',
                              blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    video_url = models.URLField(verbose_name='Ссылка на видео', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=True, null=True, verbose_name='Владелец')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='lesson_images/', verbose_name='Превью',
                              blank=True, null=True)
    video_url = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE,
                               verbose_name='Курс', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=True, null=True, verbose_name='Владелец')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Оплаченный курс',
                                    null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='Оплаченный урок',
                                    null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')

    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('bank_transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=13, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Платеж от {self.user.email} на сумму {self.paid_amount}'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
