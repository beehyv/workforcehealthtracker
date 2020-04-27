from django.db import models
class ChronicIllness(models.Model):
    illness_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.illness_name

    class Meta:
        app_label = "facility"
        verbose_name = 'Chronic Illness'

