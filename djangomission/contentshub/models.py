from django.db import models

from utils.timestamp import TimestampZone


class Master(TimestampZone):
    user = models.ForeignKey('accounts.User', verbose_name='강사 신청자', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='강사 이름', max_length=10)
    description = models.TextField(verbose_name='강사 소개', blank=True, default='')

    class Meta:
        db_table = 'master'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Klass(TimestampZone):
    master = models.ForeignKey('contentshub.Master', verbose_name='강사', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='강의 제목', max_length=50)
    description = models.TextField(verbose_name='강의 상세', blank=True, default='')

    class Meta:
        db_table = 'klass'
        ordering = ['-created_at']

    def __str__(self):
        return f'klass title: {self.title}'
