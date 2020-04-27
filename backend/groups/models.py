from django.db import models

# Create your models here.
from MyUser.models import MyUser, HCWorker
from facility.models.facility import Facility


class UserGroup(models.Model):
    name = models.CharField(max_length=100)
    facility = models.ForeignKey(Facility, null=True, verbose_name='Organization', blank=False)
    managers = models.ManyToManyField(MyUser, blank = True)
    workers = models.ManyToManyField(HCWorker, blank = True)
    is_default = models.BooleanField(default=False)

    def managers_list(self):
        return list(self.managers.filter(is_admin=False).values_list('username'))

    def workers_list(self):
        return list(self.workers.values_list('phone_number'))

