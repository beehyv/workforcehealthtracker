from django.contrib import admin

# Register your models here.
from otpvalidation.models import Otp


class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'otp')

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

admin.site.register(Otp, OtpAdmin)

