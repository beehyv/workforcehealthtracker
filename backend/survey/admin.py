from django.contrib import admin

# Register your models here.
from survey.models import SurveyInstance, Survey, SurveyQuestion, SurveyAnswer


class BaseSurveyAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions and not request.user.is_admin:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

    def has_add_permission(self, request):
        return request.user.is_admin

class SurveyAdmin(BaseSurveyAdmin):
    list_display = ('survey_name', 'question_list')

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

class SurveryInstanceAdmin(BaseSurveyAdmin):
    list_display = ('id', 'survey_date', 'result_id',)
    ordering = ('-sent_time',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin


class SurveyQuestionAdmin(BaseSurveyAdmin):
    list_display = ('survey_name', 'question_text', 'question_type')

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin


class SurveyAnswerAdmin(BaseSurveyAdmin):
    list_display = ('survey_instance', 'question_text', 'answer')

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin
    def has_add_permission(self, request):
        return request.user.is_admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyInstance, SurveryInstanceAdmin)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
admin.site.register(SurveyAnswer, SurveyAnswerAdmin)
