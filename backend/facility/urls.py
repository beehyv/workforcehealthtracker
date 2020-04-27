from django.conf.urls import url

from facility.views import FacilityList, GetFacilityByManager, HCWTypeListByOrganization

urlpatterns = [
    url(r'^getAllHCWType$', HCWTypeListByOrganization.as_view(), name="HCW Type list by organization ajax"),
    url(r'^getAll/$', FacilityList.as_view(), name="Facility list"),
    url(r'^getByManager$', GetFacilityByManager.as_view(), name="Facility by manager"),
]