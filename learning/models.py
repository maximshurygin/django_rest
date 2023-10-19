from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='course_images/', verbose_name='Превью',
                              blank=True, null=True)
    description = models.TextField(verbose_name='Описание')

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

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
