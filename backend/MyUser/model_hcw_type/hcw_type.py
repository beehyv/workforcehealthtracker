from django.db import models


class HCWType(models.Model):
    hcw_type_name = models.CharField(max_length=50, blank=False, verbose_name="Health care worker type name")

    def __str__(self):
        return self.hcw_type_name

    class Meta:
        app_label = "MyUser"
        verbose_name = "Health Care Worker Type"
