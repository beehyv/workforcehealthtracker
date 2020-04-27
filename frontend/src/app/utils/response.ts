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

export class SurveyQuestions {
  id: number;
  question_text: string;
  question_type: string;
}

export class Survey {
  id: number;
  questions: SurveyQuestions[];
}

export class HealthWorkerData {
  first_name: '';
  last_name: '';
  phone_number: '';
  whatsapp_number: '';
  employee_id: '';
  email: '';
  hcw_type_id: '';
  department: '';
  facility_id: '';
  date_of_birth: string;
  chronic_illnesses: any[];
  immunodeficiencies: any[];
  user_groups: any[];
  constructor() {}
}

export class Report {

}
// export class {
//   id: 0
//   'result_status: 'TEST ORDERED'
// }
// {
//   'first_name: 'test',
//   'last_name: 'test',
//   'phone_number: '123',
//   'whatsapp_number: '123',
//   'employee_id: '123',
//   'email: 'abc@g.com',
//   'hcw_type_id: '1',
//   'department:'test'
// }

export class GetReportList {
  count: number;
  next: string;
  previous: string;
  results: ReportList[];
}

export class ReportList {
  hcw: HCW;
  survey_list: SurveyList[];
}
export class HCW {
  id: number;
  first_name: string;
  last_name: string;
  is_active: boolean;
  phone_number: string;
  whatsapp_number: string;
  employee_id: number;
  email: string;
  department: string;
  hcw_type_id: number;
  result_status_id: number;
  date_positive: any;
  date_of_birth: any;
  user_groups: any;
  chronic_illnesses: any;
  immunodeficiencies: any;

}

export class SurveyInstance {
  id: 6;
  survey_url: string;
  survey_date: string;
  sent_time: string;
  submitted_time: string;
  survey_id: SurveyName;
  result_id: ResultName;
}
export class SurveyAnswer {
  question_text: string;
  answer: string;
}
export class SurveyList {
  survey_answers: SurveyAnswer[];
  survey_instance: SurveyInstance;
}
export class SurveyName {
  id: number;
  survey_name: string;
}
export class ResultName {
  id: number;
  result_status: string
}
export class FacilityList {
  id: number;
  facility_name: string;
  facility_type_name: string;
}
export class HwcType {
  id: number;
  hcw_type_name: string;
}
export class ResultStatus {
  id: number;
  result_status: string;
}
export class PostStatus {
  phone_number: string;
  status_id: number;
}
export class ChronicIllness {
  id: number;
  illness_name: string;
}
export class ImmunoDeficiency {
  id: number;
  deficiency_name: string;
}
// export class Groups {
//   id: number;
//   name: string;
// }
export class Filter {
  pageIndex: number;
  search_name: string;
  min_age: number;
  max_age: number;
  isImmunodeficiency: string;
  isChronicIllness: string;
  group: string;
  result_status: string;
}
export class GetAggregates {
  responded: number;
  yet_to_respond: number;
  no_action:number;
  result_pending: number;
  test_ordered: number;
  positive: number;
  negative: number;
  home_quarantine_72: number;
  precautionary_symptoms: number;
  home_quarantine_24: number;
  precuationary_general: number;
  advised_stay_home: number;
}
