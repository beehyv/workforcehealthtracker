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

from rest_framework import serializers

from MyUser.model_hcw_type.hcw_type import HCWType
from MyUser.models import ResultStatus, HCWorker
from facility.serializers import ChronicIllnessSerializer, ImmunodeficiencySerializer
from groups.serializers import UserGroupSerializer


class HCWTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HCWType
        fields = "__all__"

class ResultStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultStatus
        fields = "__all__"

class HCWorkerSerializer(serializers.ModelSerializer):
    chronic_illnesses = ChronicIllnessSerializer(many=True)
    immunodeficiencies = ImmunodeficiencySerializer(many=True)
    class Meta:
        model = HCWorker
        fields = "__all__"

class HCWorkerSurveyReportSerializer(HCWorkerSerializer):
    chronic_illnesses = ChronicIllnessSerializer(many=True)
    immunodeficiencies = ImmunodeficiencySerializer(many=True)
    user_groups = UserGroupSerializer(many=True)
    class Meta:
        model = HCWorker
        fields = "__all__"