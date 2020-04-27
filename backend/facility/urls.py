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

from django.conf.urls import url

from facility.views import FacilityList, GetFacilityByManager, HCWTypeListByOrganization

urlpatterns = [
    url(r'^getAllHCWType$', HCWTypeListByOrganization.as_view(), name="HCW Type list by organization ajax"),
    url(r'^getAll/$', FacilityList.as_view(), name="Facility list"),
    url(r'^getByManager$', GetFacilityByManager.as_view(), name="Facility by manager"),
]