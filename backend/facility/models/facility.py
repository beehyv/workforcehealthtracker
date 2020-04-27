from django.db import models

from MyUser.model_hcw_type.hcw_type import HCWType
from facility.models.communication_language import CommunicationLanguage
from facility.models.faclilityType import FacilityType


class Facility(models.Model):
    facility_name=models.CharField(max_length=100, blank=False, verbose_name='Organization Name')
    facility_type = models.ForeignKey(FacilityType, verbose_name='Organization Type')
    hcw_types = models.ManyToManyField(HCWType, null=True)
    language = models.ForeignKey(CommunicationLanguage, null=False, verbose_name='Communication Language')

    def facility_type_name(self):
        return self.facility_type.facility_type_name

    def __str__(self):
        return self.facility_name

    class Meta:
        app_label = 'facility'
        verbose_name = 'Organization'


