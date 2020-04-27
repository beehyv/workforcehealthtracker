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