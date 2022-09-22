from django.db import models

from utils.timestamp import TimestampZone


class Question(TimestampZone):
    user = models.ForeignKey('accounts.User', verbose_name='작성자', on_delete=models.CASCADE)
    klass = models.ForeignKey('contentshub.Klass', verbose_name='강의', on_delete=models.CASCADE)
    contents = models.TextField(verbose_name='질문 상세')

    class Meta:
        db_table = 'question'
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return f'question record({self.klass}-{self.user})'


class Answer(TimestampZone):
    question = models.ForeignKey('community.Question', verbose_name='질문', on_delete=models.CASCADE)
    contents = models.TextField(verbose_name='답변 상세')

    class Meta:
        db_table = 'answer'
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return f'answer record({self.question})'
