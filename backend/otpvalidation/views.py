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

import uuid

import requests
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.utils import json

from MyUser.models import HCWorker
from communications.CommunicationHandler import CommunicationHandler
from hcwtracker import settings
from otpvalidation.models import Otp
from survey.models import SurveyInstance


def send_otp(request):
    try:
        # id send otp based on survey id
        otpValue = str(uuid.uuid4()).replace('-', '')[:6]
        entity = Otp()
        entity.otp = otpValue
        instance = SurveyInstance.objects.filter(pk=request.GET['survey_id']).first()
        entity.phone_number = instance.health_worker_id.whatsapp_number
        entity.email = instance.health_worker_id.email
        commHandler = CommunicationHandler()
        commHandler.send_message(instance.health_worker_id, 5, {'otp': entity.otp})
        entity.save()
    except Exception as e:
        return HttpResponse(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = {}
    response['name'] = instance.health_worker_id.first_name
    response['consent'] = instance.health_worker_id.is_consented
    response['email'] = entity.email
    response['phone_number'] = entity.phone_number
    return JsonResponse(response)

def resend_otp(request):
    try:
        instance = SurveyInstance.objects.filter(pk=request.GET['survey_id']).first()
        worker = instance.health_worker_id
        entity = Otp.objects.filter(phone_number=worker.phone_number).order_by('-id').first()
        if entity:
            commHandler = CommunicationHandler()
            commHandler.send_message(worker, 5, {'otp': entity.otp})
    except Exception as e:
        return HttpResponse(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = {}
    response['name'] = worker.first_name
    response['consent'] = instance.health_worker_id.is_consented
    response['email'] = entity.email
    response['phone_number'] = entity.phone_number
    return JsonResponse(response)

def verify_otp(request):
    otpValue = request.GET['otp']
    phone_number = request.GET['phone_number']
    response = {}
    entity = Otp.objects.filter(phone_number=phone_number, otp=otpValue).first()

    if entity:
        worker = HCWorker.objects.filter(phone_number=phone_number).first()
        worker.is_consented = True
        worker.save()
        entity.delete()
        response['verified'] = True
    else:
        response['verified'] = False

    return JsonResponse(response)