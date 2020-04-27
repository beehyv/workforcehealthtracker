from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render


from hcwtracker import settings


def LoginView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/admin")
    return render(request, "admin/login.html")


def send_custom_email(header_type, name, message, email):
    header = settings.MESSAGES[header_type]["header"]
    message = settings.MESSAGES[header_type]["message"] + message

    message = message + "\n"
    message = message + "\n Thank you."
    message = message + "\n Healthcare Workforce team."

    final_message = "Hi " + name + ",\n" + message

    if header is not None:
        send_mail(
            header,
            final_message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True,
        )