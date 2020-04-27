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
