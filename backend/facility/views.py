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

# Create your views here.
from rest_framework import generics, permissions

from MyUser.model_hcw_type.hcw_type import HCWType
from MyUser.serializers import HCWTypeSerializer
from facility.models.chronicIllness import ChronicIllness
from facility.models.facility import Facility
from facility.models.immunodeficiency import Immunodeficiency
from facility.serializers import FacilitySerializer, ChronicIllnessSerializer, ImmunodeficiencySerializer


class FacilityList(generics.ListAPIView):
    model = Facility
    serializer_class = FacilitySerializer
    pagination_class = None

    def get_queryset(self):
        return Facility.objects.all()

class HCWTypeListByOrganization(generics.ListAPIView):
    model = HCWType
    serializer_class = HCWTypeSerializer
    pagination_class = None

    def get_queryset(self):
        id = self.request.GET['organization_id']
        return Facility.objects.filter(id=id).first().hcw_types.all()

class GetFacilityByManager(generics.RetrieveAPIView):

    model = Facility
    serializer_class = FacilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user.organization

class ChronicIllnessList(generics.ListAPIView):
    model = ChronicIllness
    serializer_class = ChronicIllnessSerializer
    pagination_class = None

    def get_queryset(self):
        return ChronicIllness.objects.all()


class ImmunodeficiencyList(generics.ListAPIView):
    model = Immunodeficiency
    serializer_class = ImmunodeficiencySerializer
    pagination_class = None

    def get_queryset(self):
        return Immunodeficiency.objects.all()
