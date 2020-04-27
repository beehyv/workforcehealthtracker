from django.db import models
from rest_framework import serializers

from MyUser.serializers import HCWorkerSurveyReportSerializer
from question.serializers.questions import QuestionSerializer
from survey.models import SurveyInstance, SurveyAnswer, SurveyReport, SurveyReportAnswerInstance


class SurveyForm(models.Model):
    username = ''
    name = ''
    survey_date = serializers.DateField()
    questions = []

    def __init__(self, username, name, questions, survey_date):
        super(SurveyForm, self).__init__()
        self.username = username
        self.name = name
        self.questions = questions
        self.survey_date = survey_date

    class Meta:
        managed = False


class SurveyFormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = SurveyForm
        fields = ('username','name', 'survey_date','questions',)
        depth = 2

class SurveyAnswerSerializer(serializers.ModelSerializer):
    survey_instance_id = serializers.CharField()
    question_id = serializers.CharField()
    answer = serializers.CharField(allow_blank=True)


    class Meta:
        model = SurveyAnswer
        fields = '__all__'
        depth = 2


class SurveyReportAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source="question_id")

    class Meta:
        model = SurveyAnswer
        fields = ("question_text", "answer",)
        depth = 2


class SurveyInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyInstance
        fields = '__all__'
        depth = 2

class SurveyReportInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyInstance
        exclude = ('health_worker_id',)
        depth = 2


class SurveyReportAnswerListSerializer(SurveyInstanceSerializer):
    survey_answers = SurveyReportAnswerSerializer(many=True)
    survey_instance = SurveyReportInstanceSerializer()
    class Meta:
        model = SurveyReportAnswerInstance
        fields = ('survey_answers', 'survey_instance')
        depth = 4


class SurveyReportSerializer(serializers.ModelSerializer):
    hcw = HCWorkerSurveyReportSerializer()
    survey_list = SurveyReportAnswerListSerializer(many=True)
    class Meta:
        model = SurveyReport
        fields = ('hcw','survey_list')
        depth = 5
