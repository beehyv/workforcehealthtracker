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

import {AbstractControl, ValidatorFn} from '@angular/forms';

const BASE_URL = '';

const URL = {
  USER_LOGIN: BASE_URL + '/login/',
  GET_SURVEY_FORM: BASE_URL + '/survey/getForm',
  GET_OTP_SCREEN: BASE_URL + '/otp/send',
  GET_RESEND_OTP: BASE_URL + '/otp/resend',
  VERIFY_OTP: BASE_URL + '/otp/verify',
  POST_SURVEY_DATA: BASE_URL + '/survey/submit',
  POST_USER_DATA: BASE_URL + '/user/createHCW/',
  UPDATE_USER_DATA: BASE_URL + '/user/updateHCW/',
  GET_REPORT: BASE_URL + '/survey/getReport',
  GET_FACILITY: BASE_URL + '/facility/getAll/',
  GET_ALL_HWC: BASE_URL + '/user/getAllHCWType/',
  GET_ALL_RESULT_STATUS: BASE_URL + '/user/getAllResultStatus/',
  GENERATE_SURVEY: BASE_URL + '/survey/generate/',
  UPDATE_STATUS: BASE_URL + '/user/updateStatus',
  WHATSAPP_API_KEY : '8ff881bb4012ac790cdb2de6586e552f-fbcf515e-4cf5-4f4e-94e1-09e39989976d',
  SEND_WHATSAPP_MESSAGE: BASE_URL + '/survey/sendWhatsappMessage',
  GET_FACILITY_BY_MANAGER : BASE_URL + '/facility/getByManager',
  GET_ALL_CHRONIC_ILLNESS : BASE_URL + '/getAllChronicIllness/',
  GET_ALL_IMMUNO_DEFICIENCY : BASE_URL + '/getAllImmunodeficiency',
  GET_ALL_GROUPS : BASE_URL + '/groups/getByManager',
  GET_AGGREGATES: BASE_URL + '/survey/getAggregates'
};

export default URL;

