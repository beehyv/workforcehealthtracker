from django.conf.urls import url

from survey import views
from survey.views import GetSurveyForm, SubmitSurvey, GetSurveyReport, send_whatsapp_message, GetSurveyAggregates

urlpatterns = [
    url(r'^submit$', SubmitSurvey.as_view(), name="Survey post"),
    url(r'^generate?', views.generate_survey, name="Generate survey"),
    url(r'^getForm?$', GetSurveyForm.as_view(), name="Get survey form"),
    url(r'^getAggregates$', GetSurveyAggregates.as_view(), name="Get Aggregates"),
    url(r'^getReport$', GetSurveyReport.as_view(), name="Get Report"),
    url(r'^sendWhatsappMessage', send_whatsapp_message, name="Send whatsapp link"),
]