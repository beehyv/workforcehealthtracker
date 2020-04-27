from django.contrib import admin

from MyUser.models import MyUser, HCWorker
from groups.models import UserGroup


# Register your models here.

class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility', 'managers_list', 'workers_list', 'is_default')

    def render_change_form(self, request, context, *args, **kwargs):
         return super(UserGroupAdmin, self).render_change_form(request, context, *args, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        facility = UserGroup.objects.get(id=request.resolver_match.args[0]).facility
        if db_field.name == "managers":
            kwargs["queryset"] = MyUser.objects.filter(organization=facility)

        if db_field.name == "workers":
            kwargs["queryset"] = HCWorker.objects.filter(facility=facility)

        return super(UserGroupAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ()
        self.exclude = ('managers', 'workers', 'is_default')
        return super(UserGroupAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ( 'is_default',)
        self.readonly_fields = ('facility',)
        if not request.user.is_admin and UserGroup.objects.get(pk=object_id).is_default:
            extra_context = extra_context or {}
            extra_context['show_delete'] = False
        return super(UserGroupAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def get_queryset(self, request):
        if request.user.is_admin:
            return UserGroup.objects

        return request.user.usergroup_set
    
    def save_model(self, request, obj, form, change):
        admins = MyUser.objects.filter(is_admin=True).all()
        obj.managers.add(*admins)
        return super(UserGroupAdmin, self).save_model(request, obj, form, change)

admin.site.register(UserGroup, UserGroupAdmin)