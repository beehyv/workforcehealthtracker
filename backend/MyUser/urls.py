from django.conf.urls import url

from MyUser.views import HCWTypeList, ResultStatusList, HCWorkerCreate, HCWWorkerUpdateStatus, HCWorkerUpdate

urlpatterns = [
    url(r'^getAllHCWType', HCWTypeList.as_view(), name="HCW Type list"),
    url(r'^getAllResultStatus', ResultStatusList.as_view(), name="Result status list"),
    url(r'^createHCW', HCWorkerCreate.as_view(), name="Health care worker creation"),
    url(r'^updateHCW', HCWorkerUpdate.as_view(), name="Health care worker update"),
    url(r'^updateStatus$', HCWWorkerUpdateStatus.as_view(), name="Health care worker status update"),

]