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

from django.contrib import admin

from facility.models.chronicIllness import ChronicIllness
from facility.models.communication_language import CommunicationLanguage
from facility.models.facility import Facility
from facility.models.faclilityType import FacilityType
from facility.models.immunodeficiency import Immunodeficiency
# Register your models here.
from groups.models import UserGroup


class FacilityAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('facility_name', 'facility_type_name')
    search_fields = ('name','facility_type_name' )
    list_filter = ('facility_type',)

    def save_model(self, request, obj, form, change):
        super(FacilityAdmin, self).save_model(request, obj, form, change)
        usergroup = UserGroup()
        usergroup.facility = obj
        usergroup.name = obj.facility_name + " group"
        usergroup.is_default = True
        usergroup.save()
        usergroup.managers.add(request.user)

    def has_add_permission(self, request):
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

class FacilityTypeAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('facility_type_name',)
    search_fields = ('facility_type_name',)

    def has_add_permission(self, request):
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin


class CommunicationLanguageAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('language_name',)
    search_fields = ('language_name',)


    def has_add_permission(self, request):
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin


class ChronicIllnessAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('illness_name',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

class ImmunodeficiencyAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('deficiency_name',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

admin.site.register(ChronicIllness, ChronicIllnessAdmin)
admin.site.register(Immunodeficiency, ImmunodeficiencyAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(FacilityType, FacilityTypeAdmin)
admin.site.register(CommunicationLanguage, CommunicationLanguageAdmin)