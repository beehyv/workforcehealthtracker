from django.db import models

# Create your models here.
class QuestionType(models.Model):
    question_type = models.CharField(max_length=10)

    def __str__(self):
        return self.question_type

    class Meta:
        app_label = 'question'
        verbose_name = 'Question Type'


class Question(models.Model):
    question_type_id = models.ForeignKey(QuestionType)
    question_text = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.question_type_id.question_type + " -- " + self.question_text

    class Meta:
        app_label = 'question'
        verbose_name = 'Question'