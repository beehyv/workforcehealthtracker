from django.db import models

class Immunodeficiency(models.Model):
    deficiency_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.deficiency_name

    class Meta:
        app_label = "facility"
        verbose_name = 'Immunodeficiency'

