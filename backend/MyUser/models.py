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

import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from MyUser.model_hcw_type.hcw_type import HCWType
from facility.models.chronicIllness import ChronicIllness
from facility.models.communication_language import CommunicationLanguage
from facility.models.facility import Facility
from facility.models.immunodeficiency import Immunodeficiency


class ResultStatus(models.Model):
    result_status = models.CharField(max_length=50, blank=False, verbose_name="Result status")
    result_message = models.CharField(max_length=500, blank=True, verbose_name="Result message", null=True)

    def __str__(self):
        return self.result_status

    class Meta:
        app_label = "MyUser"
        verbose_name = "Result status"
        verbose_name_plural = "Result statuses"


class MyUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None, email=None, whatsapp_number=None):
        """
        Creates and saves a Myuser with the given email, date of
        birth and password.
        """

        if not username:
            raise ValueError('Users must have phone number')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            whatsapp_number=whatsapp_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password=None, email=None, whatsapp_number=None):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            whatsapp_number=whatsapp_number,
            is_admin=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(
        verbose_name='email',
        max_length=255, null=True, blank=True
    )
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="Global Administrator")
    objects = MyUserManager()
    username = models.CharField(max_length=10, unique=True, verbose_name='Phone Number')
    whatsapp_number = models.CharField(max_length=10, blank=True, verbose_name='Whatsapp Number', null=True, default=0)
    language = models.ForeignKey(CommunicationLanguage)
    organization = models.ForeignKey(Facility, verbose_name='Organization')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        s = self.first_name
        s = s + "(" + self.organization.facility_name + ")"

        return s

    def assigned_facility(self):
        if self.organization is None:
            return "-"
        return self.organization.facility_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return True

    class Meta:
        app_label = 'MyUser'
        verbose_name = 'Health Care Manager'


class HCWorker(models.Model):

    def validate_date_of_birth(value):

        years = datetime.datetime.today().year - value.year
        if years < 18:
            raise ValidationError('Age is cannot be less than 18 years')

        if years > 120:
            raise ValidationError('Age is cannot be more than 120 years')
        pass

    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=10, blank=False, unique=True)
    whatsapp_number = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=False, blank=False, validators=[validate_date_of_birth])
    facility = models.ForeignKey(Facility, verbose_name='Organization')
    hcw_type_id = models.ForeignKey(HCWType, verbose_name="Job Title")
    result_status_id = models.ForeignKey(ResultStatus, null=True)
    employee_id = models.CharField(max_length=50, null=True)
    email = models.EmailField(blank=True, null=True)
    department= models.CharField(max_length=50, blank=True)
    date_positive = models.DateTimeField(null=True, blank=True)
    chronic_illnesses = models.ManyToManyField(ChronicIllness, blank=True)
    immunodeficiencies = models.ManyToManyField(Immunodeficiency, blank=True)
    is_consented = models.BooleanField(default=False)
    language = models.ForeignKey(CommunicationLanguage)
    telegram_username = models.CharField(max_length=50, null=True, blank=True, verbose_name='Telegram username')
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']


    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        s = self.first_name
        s = s + "(" + self.facility.facility_name + ")"

        return s

    def user_groups(self):
        return self.usergroup_set.all()

    class Meta:
        app_label = 'MyUser'
        verbose_name = 'Health Care Worker'

