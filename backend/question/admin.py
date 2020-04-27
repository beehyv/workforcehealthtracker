from django.contrib import admin
# Register your models here.
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

from question.models import QuestionType, Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ( 'question_text', 'question_type_id', )
    list_filter = ('question_type_id',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

admin.site.register(Question, QuestionAdmin)


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('question_type',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.unregister(Group)
admin.site.unregister(Token)