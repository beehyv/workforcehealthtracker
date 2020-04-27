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