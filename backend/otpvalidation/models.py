from django.db import models

class Otp(models.Model):
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)

    class Meta:
        app_label = "otpvalidation"
        verbose_name = 'OTP'
