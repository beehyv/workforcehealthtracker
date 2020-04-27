/*
 *  Licensed to the Apache Software Foundation (ASF) under one
 *  or more contributor license agreements.  See the NOTICE file
 *  distributed with this work for additional information
 *  regarding copyright ownership.  The ASF licenses this file
 *  to you under the Apache License, Version 2.0 (the
 *  "License"); you may not use this file except in compliance
 *  with the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing,
 *  software distributed under the License is distributed on an
 *  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 *  KIND, either express or implied.  See the License for the
 *  specific language governing permissions and limitations
 *  under the License.
 *
 *  Built and managed with Open Source Love by BeeHyv Software Solutions Pvt Ltd. Hyderabad
 *  www.beehyv.com
 */

import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import URL from './UrlUtills';
import {ChronicIllness, FacilityList, Filter, GetAggregates, GetReportList, HwcType, ImmunoDeficiency, ResultStatus} from './response';

@Injectable({
  providedIn: 'root'
})
export class FetchDataService {

  constructor(private http: HttpClient) { }
  login(username: string, password: string, successCallback, errorCallback) {
    const user = {username, password};
    const url = URL.USER_LOGIN;
    return this.http.post(url, user, {observe: 'response'})
      .subscribe((response) => {
        if (response) {
          successCallback(response);
        } else {
          errorCallback();
        }
      }, () => {
        errorCallback();
      });
  }

  getHeader() {
    return new HttpHeaders({
      Authorization: 'Token ' + localStorage.getItem('authToken')
    });
  }

  postSurveyData(surveyData, successCallback, errorCallback) {
    const url = URL.POST_SURVEY_DATA;
    return this.http.post(url, surveyData, {observe: 'response'})
      .subscribe((response) => {
        successCallback(response);
      }, (error) => {
        if (error.status === 201) {
          successCallback();
        } else {
          errorCallback();
        }
      });
  }
  postHealthWorkerData(surveyData) {
    const url = URL.POST_USER_DATA;
    return this.http.post(url, surveyData, {headers: this.getHeader()});
  }
  updateHealthWorkerData(surveyData) {
    const url = URL.UPDATE_USER_DATA;
    return this.http.post(url, surveyData, {headers: this.getHeader()});
  }
  postStatus(statusData) {
    const url = URL.UPDATE_STATUS;
    return this.http.post(url, statusData, {headers: this.getHeader()});
  }
  getSurveyForm(surveyId) {
    const url = URL.GET_SURVEY_FORM + '?survey_id=' + surveyId;
    return this.http.get(url);
  }
  getOTPScreen(surveyId) {
    const url = URL.GET_OTP_SCREEN + '?survey_id=' + surveyId;
    return this.http.get(url, {headers: this.getHeader()});
  }
  getResendOTP(surveyId) {
    const url = URL.GET_RESEND_OTP + '?survey_id=' + surveyId;
    return this.http.get(url, {headers: this.getHeader()});
  }
  verifyOTP(survey_id, otp) {
    const url = URL.VERIFY_OTP + '?survey_id=' + survey_id + '&otp=' + otp;
    return this.http.get(url, {headers: this.getHeader()});
  }
  getReport(filter: Filter) {
    const url = URL.GET_REPORT;
    return this.http.get<GetReportList>(url, {
      headers: this.getHeader(),
      params: {
        page: String(filter.pageIndex),
        search_name : filter.search_name ? filter.search_name : '',
        immunodeficiency: filter.isImmunodeficiency ? filter.isImmunodeficiency : '',
        chronic_illness: filter?.isChronicIllness ? filter.isChronicIllness : '',
        age_minimum: filter?.min_age ? filter.min_age.toString() : '',
        age_maximum: filter?.max_age ? filter.max_age.toString() : '',
        user_groups: filter?.group ? filter.group.replace(/,\s*$/, "") : '',
        result_status: filter?.result_status ? filter.result_status : ''
      }
    });
  }
  // searchReport(searchReport, pageIndex: number) {
  //   const url = URL.GET_REPORT;
  //   return this.http.get<GetReportList>(url, {
  //     headers: this.getHeader(),
  //     params: {
  //       page: String(pageIndex),
  //       search_name: searchReport
  //     }
  //   });
  // }
  getAllFacility() {
    const url = URL.GET_FACILITY;
    return this.http.get<FacilityList[]>(url,{headers: this.getHeader()});
  }
  getAllHwcType() {
    const url = URL.GET_ALL_HWC;
    return this.http.get<HwcType[]>(url,{headers: this.getHeader()});
  }
  getResultStatus() {
    const url = URL.GET_ALL_RESULT_STATUS;
    return this.http.get<ResultStatus[]>(url,{headers: this.getHeader()});
  }
  generateSurvey(phone_number) {
    const url = URL.GENERATE_SURVEY + '?phone_number=' + phone_number;
    return this.http.get<string>(url,{headers: this.getHeader()});
  }
  sendWhatsAPP(phone_number) {
    const url = URL.SEND_WHATSAPP_MESSAGE + '?phone_number=' + phone_number;
    return this.http.get<string>(url, {headers: this.getHeader()});
  }
  getfaciltityByManager() {
    const url = URL.GET_FACILITY_BY_MANAGER;
    return this.http.get(url, {headers: this.getHeader()});
  }
  getAllChronicIllness() {
    const url = URL.GET_ALL_CHRONIC_ILLNESS;
    return this.http.get<ChronicIllness[]>(url, {headers: this.getHeader()});
  }
  getAllImmunoDefeciency() {
    const url = URL.GET_ALL_IMMUNO_DEFICIENCY;
    return this.http.get<ImmunoDeficiency[]>(url, {headers: this.getHeader()});
  }
  getAllGroups() {
    const url = URL.GET_ALL_GROUPS;
    return this.http.get<any[]>(url, {headers: this.getHeader()});
  }
  getAggregates() {
    const url = URL.GET_AGGREGATES;
    return this.http.get<GetAggregates>(url, {headers: this.getHeader()});
  }
}
