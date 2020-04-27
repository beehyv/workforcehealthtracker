"""hcwtracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

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

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

from facility.views import ChronicIllnessList, ImmunodeficiencyList

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^accounts/login/$', LoginView),
    url(r'^survey/', include('survey.urls')),
    url(r'^user/', include('MyUser.urls')),
    url(r'^facility/', include('facility.urls')),
    url(r'^groups/', include('groups.urls')),
    url(r'^otp/', include('otpvalidation.urls')),
    url(r'^login/', obtain_auth_token, name='api_token_auth'),
    url(r'^getAllChronicIllness/', ChronicIllnessList.as_view(), name='Chronic illness'),
    url(r'^getAllImmunodeficiency/', ImmunodeficiencyList.as_view(), name='Immunodeficiency list'),

]
