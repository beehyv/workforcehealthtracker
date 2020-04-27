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
