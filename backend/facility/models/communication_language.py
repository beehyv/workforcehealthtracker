from django.db import models


class CommunicationLanguage(models.Model):
    language_name = models.CharField(max_length=50, blank=False, verbose_name='Language name')

    def __str__(self):
        return self.language_name

    class Meta:
        app_label = "facility"
