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

import datetime
import json

import requests
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework import generics, status, permissions

from MyUser.models import HCWorker, ResultStatus
from communications.CommunicationHandler import CommunicationHandler
from hcwtracker import settings
from question.models import Question
from survey.models import SurveyInstance, Survey, SurveyQuestion, SurveyAnswer, SurveyReport, SurveyReportAnswerInstance
from survey.serializers.surveyForm import SurveyForm, SurveyFormSerializer, \
    SurveyAnswerSerializer, SurveyReportSerializer


class SubmitSurvey(generics.CreateAPIView):
    model = SurveyForm
    serializer_class = SurveyInstance

    def post(self, request, *args, **kwargs):
        serializer = SurveyAnswerSerializer(data=request.data, many=True)
        if request.data is None or len(request.data) == 0:
            return HttpResponse("No request body", status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            try:
                survey_id = None
                for data in list(serializer.data):
                    survey_id = data['survey_instance_id']

                survey_instance = SurveyInstance.objects.filter(id=survey_id).first()
                if survey_instance is not None and survey_instance.submitted_time is not None:
                    return HttpResponse("Survey already submitted for survey id " + str(survey_id),
                                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    A1 = 0
                    A2 = 0
                    A3 = 0
                    B = 0
                    C = 0
                    for data in list(serializer.data):
                        question_id = data['question_id']
                        answer = data['answer']
                        survey_answer = SurveyAnswer(survey_instance_id_id=survey_id,
                                                     question_id_id=str(question_id), answer=answer)
                        if int(question_id) == 1: A1 = int(answer)
                        if int(question_id) == 2: A2 = int(answer)
                        if int(question_id) == 10: A3 = int(answer)
                        if int(question_id) == 8: C = int(answer)
                        if int(question_id) == 9: B = int(answer)
                        survey_answer.save()

                    if survey_id is not None:
                        survey_instance = SurveyInstance.objects.filter(id=survey_id).first()
                        survey_instance.submitted_time = datetime.datetime.now()

                        health_worker = survey_instance.health_worker_id
                        if health_worker is not None \
                                and health_worker.result_status_id is not None \
                                and health_worker.result_status_id.id \
                                in [3, 4, 5, 6]:  # todo change to enum
                            survey_instance.result_id = health_worker.result_status_id
                        else:
                            """
                                triaging logic
                            """
                            result_id = 1
                            age = datetime.datetime.now().year - health_worker.date_of_birth.year

                            if ((A1 + A2 + A3 == 1) or (A1 + A2 + A3 == 2)) \
                                    and (B + C == 0):
                                if age >= 60:
                                    result_id = 7  # quarantine - 72 hours contact
                                else:
                                    result_id = 8  # precaution - you have symptoms
                            else:
                                if (A1 + A2 + A3 == 3) or B == 1 or C == 1:
                                    result_id = 9  # quarantine - 24 hours contact
                                else:
                                    if health_worker.immunodeficiencies.count() > 0:
                                        if age >= 60:
                                            result_id = 11  # stay at home
                                        else:
                                            result_id = 10

                            survey_instance.result_id = ResultStatus.objects.filter(
                                id=result_id).first()

                        survey_instance.save()
                        health_worker.result_status_id = survey_instance.result_id
                        health_worker.save()

                        result_id = health_worker.result_status_id.id
                        if result_id != 1:
                            if result_id >= 7:
                                message = ""
                                if result_id == 7:
                                    message = "Please follow home quarantine protocol and make a call or update the survey after 72 hours to check for symptoms"
                                if result_id == 8:
                                    message = "Please take precautionary measures like handwashing and social distancing. Call you back or update survey immediately if all 3 symptoms show up"
                                if result_id == 9:
                                    message = "After 24 hours call or update the survey, to check for symptoms"
                                if result_id == 10:
                                    message = "Take precautionary measures like handwashing and social distancing."
                                if result_id == 11:
                                    message = "The advice will be to stay at home, and the district office will send a doctor to their home to do a checkup."
                                commHandler = CommunicationHandler()
                                commHandler.send_message(health_worker, 1, {'health_status': message})

                            else:
                                message = "Your status is still " + health_worker.result_status_id.result_status
                                commHandler = CommunicationHandler()
                                commHandler.send_message(health_worker, 4, {})
            except Exception as e:
                return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse("Invalid data", status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(survey_instance.result_id, status=status.HTTP_201_CREATED)


"""
    input would consist of
    user,
    survey
"""


def generate_survey(request):
    if request.GET['phone_number'] is None:
        return HttpResponse("Missing phone number", status=status.HTTP_400_BAD_REQUEST)

    health_worker = HCWorker.objects.filter(phone_number=request.GET['phone_number']).first()
    survey_instance = SurveyInstance.objects.filter(health_worker_id_id=health_worker.id,
                                                    survey_date=datetime.date.today()).order_by('-survey_date',
                                                                                                '-id').first()

    if survey_instance is not None and survey_instance.submitted_time is None:
        return HttpResponse(survey_instance.survey_url)
    else:
        instance = SurveyInstance()
        instance.health_worker_id = health_worker
        instance.survey_id = Survey.objects.all().first()
        instance.survey_date = datetime.date.today()
        instance.submitted_time = None
        instance.result_id = None
        instance.sent_time = datetime.datetime.now()
        instance.save()
        instance.survey_url = '/survey/getForm?survey_id=' + str(instance.id)
        instance.save(force_update=True)
        return HttpResponse(instance.survey_url)


"""
    survey instance id would be sent as a query parameter
"""


class GetSurveyForm(generics.RetrieveAPIView):
    model = SurveyForm
    serializer_class = SurveyFormSerializer

    def get_object(self):
        if self.request.GET['survey_id'] is None:
            return None
        survey_instance = SurveyInstance.objects.filter(pk=self.request.GET['survey_id']).first()
        if survey_instance is None:
            return None
        survey = survey_instance.survey_id
        question_ids = list(SurveyQuestion.objects.filter(survey_id=survey.id).values_list('question_id', flat=True))
        questions = list(Question.objects.filter(id__in=question_ids))
        return SurveyForm(survey_instance.health_worker_id.first_name, survey.survey_name, questions,
                          survey_instance.survey_date)


class GetSurveyReport(generics.ListAPIView):
    model = SurveyReport
    serializer_class = SurveyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        response = []
        user = self.request.user
        hcw_set = set()
        for group in user.usergroup_set.all():
            for hcw in group.workers.all():
                hcw_set.add(hcw.id)

        try:
            query_params = self.request.query_params
            search_name = query_params.get('search_name')
            immunodeficiency = query_params.get('immunodeficiency')
            chronic_illness = query_params.get('chronic_illness')
            age_minimum = query_params.get('age_minimum')
            age_maximum = query_params.get('age_maximum')
            result_status = query_params.get('result_status')
            user_groups = query_params.get('user_groups')

            query = Q(id__in=hcw_set)
            if search_name:
                q_search_name = Q(first_name__icontains=search_name)
                query = query & q_search_name
            if immunodeficiency:
                q_immunodeficiency = Q(immunodeficiencies__isnull=(immunodeficiency != 'true'))
                query = query & q_immunodeficiency
            if chronic_illness:
                q_chronic_illness = Q(chronic_illnesses__isnull=(chronic_illness != 'true'))
                query = query & q_chronic_illness
            if age_minimum:
                dob_minimum = datetime.datetime.today() - datetime.timedelta(365 * int(age_minimum))
                q_age_minimum = Q(date_of_birth__lt=dob_minimum)
                query = query & q_age_minimum
            if age_maximum:
                dob_maximum = datetime.datetime.today() - datetime.timedelta(365 * int(age_maximum))
                dob_maximum = dob_maximum.replace(month=1, day=1)
                q_age_maximum = Q(date_of_birth__gt=dob_maximum)
                query = query & q_age_maximum
            if result_status:
                q_result_status = Q(result_status_id_id=result_status)
                query = query & q_result_status
            if user_groups:
                ug_list = []
                for group in user_groups.split(','):
                    ug_list.append(int(group))
                q_user_groups = Q(usergroup__in=ug_list)
                query = query & q_user_groups

            hcw_queryset = HCWorker.objects.filter(query).distinct()
        except Exception as e:
            return HttpResponse("Error in query param" + str(e), status=status.HTTP_400_BAD_REQUEST)

        for hcw in hcw_queryset:
            report_answer_instance_list = []  # survey_list

            db_instance_list = list(SurveyInstance.objects.filter(health_worker_id=hcw.id).all())
            for instance in db_instance_list:
                survey_answer = list(SurveyAnswer.objects.filter(survey_instance_id=instance.id).all())
                report_answer_instance_list.append(SurveyReportAnswerInstance(survey_answer, instance))

            report = SurveyReport(hcw, report_answer_instance_list)
            response.append(report)

        return response


def send_whatsapp_message(request):
    if request.GET['phone_number'] is None:
        return HttpResponse("Missing phone number", status=status.HTTP_400_BAD_REQUEST)

    health_worker = HCWorker.objects.filter(phone_number=request.GET['phone_number']).first()
    survey_instance = SurveyInstance.objects.filter(health_worker_id_id=health_worker.id,
                                                    survey_date=datetime.date.today()).order_by('-survey_date',
                                                                                                '-id').first()
    response = {}
    if survey_instance is not None and survey_instance.submitted_time is None:
        response['survey_id'] = survey_instance.id
    else:
        instance = SurveyInstance()
        instance.health_worker_id = health_worker
        instance.survey_id = Survey.objects.all().first()
        instance.survey_date = datetime.date.today()
        instance.submitted_time = None
        instance.result_id = None
        instance.sent_time = datetime.datetime.now()
        instance.save()
        instance.survey_url = '/survey/getForm?survey_id=' + str(instance.id)
        instance.save(force_update=True)
        response['survey_id'] = instance.id

    whatsapp_number = health_worker.whatsapp_number
    response['whatsapp_number'] = whatsapp_number

    commHandler = CommunicationHandler()
    commHandler.send_message(health_worker, 2, {
        'survey_link': settings.FRONTEND_URL + "/#/survey?survey_id=" + str(response['survey_id'])})

    return JsonResponse(response)


class GetSurveyAggregates(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        manager = request.user
        hcw_set_id = set()
        hcw_set = set()
        for group in manager.usergroup_set.all():
            for hcw in group.workers.all():
                hcw_set.add(hcw)
                hcw_set_id.add(hcw.id)

        survey_instances = SurveyInstance.objects.filter(health_worker_id__in=hcw_set_id,
                                                         survey_date=datetime.datetime.today()).order_by(
            '-submitted_time').all()

        aggrs = {
            'responded': 0,
            'yet_to_respond': 0,
            'no_action': 0,
            'result_pending': 0,
            'test_ordered': 0,
            'positive': 0,
            'negative': 0,
            'home_quarantine_72': 0,
            'precautionary_symptoms': 0,
            'home_quarantine_24': 0,
            'precuationary_general': 0,
            'advised_stay_home': 0
        }

        surveys = {}
        for inst in survey_instances:
            if surveys[inst.hcworker_id.id] is None:
                surveys[inst.hcworker_id.id] = []
            surveys[inst.hcworker_id.id].append(inst)

        for hcw in hcw_set:
            survey_list = surveys.get(hcw.id)
            # submitted
            if survey_list and len(survey_list) > 1 and survey_list[0].submitted_time is not None:
                aggrs['responded'] += 1
            else:
                aggrs['yet_to_respond'] += 1

        for hcw in hcw_set:
            result_id = hcw.result_status_id
            if result_id is None or result_id.id == 1:
                aggrs['no_action'] += 1
            else:
                result_id = result_id.id
                if result_id == 3:
                    aggrs['result_pending'] += 1
                if result_id == 4:
                    aggrs['positive'] += 1
                if result_id == 5:
                    aggrs['negative'] += 1
                if result_id == 6:
                    aggrs['test_ordered'] += 1
                if result_id == 7:
                    aggrs['home_quarantine_72'] += 1
                if result_id == 8:
                    aggrs['precautionary_symptoms'] += 1
                if result_id == 9:
                    aggrs['home_quarantine_24'] += 1
                if result_id == 10:
                    aggrs['precuationary_general'] += 1
                if result_id == 11:
                    aggrs['advised_stay_home'] += 1

        return JsonResponse(aggrs)
