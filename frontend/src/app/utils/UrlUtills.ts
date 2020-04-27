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

