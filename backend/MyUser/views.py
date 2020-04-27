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
from django.http import HttpResponse
# Create your views here.
from rest_framework import generics, status, permissions

from MyUser.model_hcw_type.hcw_type import HCWType
from MyUser.models import HCWorker, ResultStatus
from MyUser.serializers import HCWTypeSerializer, ResultStatusSerializer, HCWorkerSerializer
from communications.CommunicationHandler import CommunicationHandler
from facility.models.chronicIllness import ChronicIllness
from facility.models.immunodeficiency import Immunodeficiency
from groups.models import UserGroup


class HCWTypeList(generics.ListAPIView):
    model = HCWType
    serializer_class = HCWTypeSerializer
    pagination_class = None

    def get_queryset(self):
        manager = self.request.user
        return manager.organization.hcw_types.all()

class ResultStatusList(generics.ListAPIView):
    model = ResultStatus
    serializer_class = ResultStatusSerializer
    pagination_class = None

    def get_queryset(self):
        return ResultStatus.objects.all()

class HCWorkerCreate(generics.CreateAPIView):
    model = HCWorker
    serializer_class = HCWorkerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        req_data = request.data
        if HCWorker.objects.filter(phone_number=req_data['phone_number']).first() is not None:
            return HttpResponse("User already exists. Change phone number",status=status.HTTP_400_BAD_REQUEST)

        hcw_type_id = req_data.pop('hcw_type_id')
        chronic_illnesses = req_data.pop('chronic_illnesses')
        immunodeficiencies = req_data.pop('immunodeficiencies')
        user_group_ids = req_data.pop('user_groups')
        if req_data.get('facility_id'):
            req_data.pop('facility_id')

        default_group = request.user.usergroup_set.filter(is_default=True).first()
        facility = default_group.facility
        health_worker = HCWorker.objects.create(hcw_type_id_id=hcw_type_id, language=facility.language, facility=facility, **req_data)
        try :
            if health_worker is None:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            health_worker.result_status_id = ResultStatus.objects.filter(pk=1).first()

            if chronic_illnesses is not None:
                chronic_illnesses_instances = ChronicIllness.objects.filter(pk__in=chronic_illnesses).all()
                health_worker.chronic_illnesses.add(*chronic_illnesses_instances)

            if immunodeficiencies is not None:
                immunodeficiency_instances = Immunodeficiency.objects.filter(pk__in=immunodeficiencies).all()
                health_worker.immunodeficiencies.add(*immunodeficiency_instances)

            if user_group_ids is not None:
                user_group_instances = UserGroup.objects.filter(pk__in=user_group_ids).all()
                health_worker.usergroup_set.add(*user_group_instances)

            health_worker.usergroup_set.add(default_group)

            return HttpResponse("Success", status=status.HTTP_201_CREATED)
        except Exception as e:
            health_worker.delete()
            return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

class HCWorkerUpdate(generics.CreateAPIView):
    model = HCWorker
    serializer_class = HCWorkerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        req_data = request.data
        instance = HCWorker.objects.filter(id=req_data['id']).first()
        if instance is None:
            return HttpResponse("User doesnt exists.",status=status.HTTP_400_BAD_REQUEST)

        try :

            default_group = request.user.organization.usergroup_set.first()

            existing_worker = HCWorker.objects.filter(phone_number=req_data['phone_number']).first()
            if existing_worker is not None and existing_worker.id != instance.id:
                return HttpResponse("Mobile number already taken.", status=status.HTTP_400_BAD_REQUEST)
            hcw_type_id = req_data.pop('hcw_type_id')
            chronic_illnesses = req_data.pop('chronic_illnesses')
            immunodeficiencies = req_data.pop('immunodeficiencies')
            user_group_ids = req_data.pop('user_groups')
            if req_data.get('facility_id'):
                req_data.pop('facility_id')
            if req_data.get('facility'):
                req_data.pop('facility')
            HCWorker.objects.filter(id=req_data['id']).update(hcw_type_id_id=hcw_type_id, facility=default_group.facility, **req_data)

            if instance is None:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            if chronic_illnesses is None:
                chronic_illnesses = []
            chronic_illnesses_instances = ChronicIllness.objects.filter(pk__in=chronic_illnesses).all()
            instance.chronic_illnesses.clear()
            instance.chronic_illnesses.add(*chronic_illnesses_instances)

            if immunodeficiencies is None:
                immunodeficiencies = []
            immunodeficiencies_instances = Immunodeficiency.objects.filter(pk__in=immunodeficiencies).all()
            instance.immunodeficiencies.clear()
            instance.immunodeficiencies.add(*immunodeficiencies_instances)

            if user_group_ids is None:
                user_group_ids = []
            user_group_instances = UserGroup.objects.filter(pk__in=user_group_ids).all()
            instance.usergroup_set.clear()
            instance.usergroup_set.add(*user_group_instances)
            instance.usergroup_set.add(default_group)

            return HttpResponse("Success", status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HCWWorkerUpdateStatus(generics.ListAPIView):
    model = HCWorker
    serializer_class = HCWorkerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        req_data = request.data
        phone_number = req_data['phone_number']
        status_id = req_data['status_id']
        if phone_number is None:
            return HttpResponse("Phone number missing", status=status.HTTP_400_BAD_REQUEST)
        if status_id is None:
            return HttpResponse("Status id missing", status=status.HTTP_400_BAD_REQUEST)
        if int(status_id) == 0:
            return HttpResponse("Status id cannot be zero", status=status.HTTP_400_BAD_REQUEST)

        hcw = HCWorker.objects.filter(phone_number=phone_number).first()
        if hcw is None:
            return HttpResponse("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        for result_status in ResultStatus.objects.all():
            if result_status.id == status_id:
                hcw.result_status_id = result_status
                break
        if status_id == ResultStatus.objects.filter(result_status="POSITIVE").first().id:
            hcw.date_positive = datetime.datetime.now()
        hcw.save()

        message = None
        if status_id == 7:
            message = "Please follow home quarantine protocol and make a call or update the survey after 72 hours to check for symptoms"
        if status_id == 8:
            message = "Please take precautionary measures like handwashing and social distancing. Call you back or update survey immediately if all 3 symptoms show up"
        if status_id == 9:
            message = "After 24 hours call or update the survey, to check for symptoms"
        if status_id == 10:
            message = "Take precautionary measures like handwashing and social distancing."
        if status_id == 11:
            message = "The advice will be to stay at home, and the district office will send a doctor to their home to do a checkup."
        if status_id == 3:
            message = "Results Pending"
        if status_id == 4:
            message = "Tested Positive"
        if status_id == 5:
            message = "Tested Negative"
        if status_id == 6:
            message = "New test ordered"

        if message is not None:
            commHandler = CommunicationHandler()
            commHandler.send_message(hcw, 3, {"new_status": message})

        return HttpResponse("Success", status=status.HTTP_200_OK)

