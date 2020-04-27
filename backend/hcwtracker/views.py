#   Licensed to the Apache Software Foundation (ASF) under one
#   or more contributor license agreements.  See the NOTICE file
#   distributed with this work for additional information
#   regarding copyright ownership.  The ASF licenses this file
#   to you under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in compliance
#   with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing,
#   software distributed under the License is distributed on an
#   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#   KIND, either express or implied.  See the License for the
#   specific language governing permissions and limitations
#   under the License.
#
#   Built and managed with Open Source Love by BeeHyv Software Solutions Pvt Ltd. Hyderabad
#   www.beehyv.com

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