from django.conf.urls import url

from otpvalidation.views import send_otp, resend_otp, verify_otp

urlpatterns = [
    url(r'^send', send_otp, name="send otp"),
    url(r'^resend', resend_otp, name="resend otp"),
    url(r'^verify', verify_otp, name="verify otp"),
]