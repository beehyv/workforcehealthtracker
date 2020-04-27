from rest_framework import serializers

from facility.models.chronicIllness import ChronicIllness
from facility.models.facility import Facility
from facility.models.immunodeficiency import Immunodeficiency


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ('id','facility_name', 'facility_type_name')
        depth = 1

class ChronicIllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicIllness
        fields = ('id', 'illness_name')


class ImmunodeficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Immunodeficiency
        fields = ('id', 'deficiency_name')
