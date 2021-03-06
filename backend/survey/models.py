#   Licensed to the Apache Software Foundation (ASF) under one
#   or more contributor license agreements.  See the NOTICE file
#   distributed with this work for additional information
#   regarding copyright ownership.  The ASF licenses this file
#   to you under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in compliance
#   with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing,
#   software distributed under the License is distributed on an
#   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#   KIND, either express or implied.  See the License for the
#   specific language governing permissions and limitations
#   under the License.
#
#   Built and managed with Open Source Love by BeeHyv Software Solutions Pvt Ltd. Hyderabad
#   www.beehyv.com

from django.db import models

from MyUser.models import HCWorker, ResultStatus
from question.models import Question


class Survey(models.Model):
    survey_name = models.CharField(max_length=100)

    def __str__(self):
        return self.survey_name

    def question_list(self):
        question_list = []
        questions = SurveyQuestion.objects.filter(survey_id=self.id).all()
        for question in questions:
            question_list.append(question.question_id)
        return question_list

    class Meta:
        app_label = 'survey'
        verbose_name = 'Survey'

class SurveyQuestion(models.Model):
    survey_id = models.ForeignKey(Survey)
    question_id = models.ForeignKey(Question)

    def question_text(self):
        return self.question_id.question_text

    def question_type(self):
        return self.question_id.question_type_id.question_type

    def survey_name(self):
        return self.survey_id.survey_name

    class Meta:
        app_label = 'survey'
        verbose_name = 'Survey Question'


class SurveyInstance(models.Model):
    survey_id = models.ForeignKey(Survey)
    health_worker_id = models.ForeignKey(HCWorker)
    survey_url = models.CharField(max_length=500)
    survey_date = models.DateTimeField(null=True)
    sent_time = models.DateTimeField(null=True)
    submitted_time = models.DateTimeField(null=True)
    result_id = models.ForeignKey(ResultStatus, null=True)

    def __str__(self):
        return self.health_worker_id.phone_number + " -- " + str(self.survey_id.id)

    class Meta:
        app_label = 'survey'
        verbose_name = 'Survey Instance'


class SurveyAnswer(models.Model):
    survey_instance_id = models.ForeignKey(SurveyInstance)
    question_id = models.ForeignKey(Question)
    answer = models.CharField(max_length=100, blank=True)

    def question_text(self):
        return self.question_id.question_text

    def survey_instance(self):
        return self.survey_instance_id.id

    class Meta:
        app_label = 'survey'
        verbose_name = 'Survey Answer'



class SurveyReport(models.Model):
    hcw = HCWorker()
    survey_list = [] #SurveyReportAnswerInstance

    def __init__(self, hcw, survey_list):
        super(SurveyReport, self).__init__()
        self.hcw = hcw
        self.survey_list = survey_list


    class Meta:
        managed = False

class SurveyReportAnswerInstance(models.Model):
    survey_answers = [] #SurveyReportAnswerInstance
    survey_instance = SurveyInstance()

    def __init__(self, survey_answers, survey_instance):
        super(SurveyReportAnswerInstance, self).__init__()
        self.survey_answers = survey_answers
        self.survey_instance = survey_instance

    class Meta:
        managed = False
