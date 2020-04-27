from django.db import models


class FacilityType(models.Model):
    facility_type_name = models.CharField(max_length=50, blank=False, verbose_name='Organization type name')

    def __str__(self):
        return self.facility_type_name

    class Meta:
        app_label = "facility"
        verbose_name = 'Organization Type'
