from django.conf.urls import url

from groups.views import UserGroupList, UserGroupListByManager

urlpatterns = [
    url(r'^getAll$', UserGroupList.as_view(), name="Facility list"),
    url(r'^getByManager', UserGroupListByManager.as_view(), name="Facility by manager"),
]