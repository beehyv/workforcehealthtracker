from rest_framework import serializers

from question.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    question_text = serializers.CharField()
    question_type = serializers.CharField(source="question_type_id")

    class Meta:
        model = Question
        fields = ('id','question_text', 'question_type',)
        depth = 1