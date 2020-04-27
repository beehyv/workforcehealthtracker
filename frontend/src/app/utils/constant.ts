import {Report} from './response';

export const REPORT = [{
  symptom: 'cough',
  value : 'yes',
}, {
  symptom: 'shortness_of_breath',
  value : 'yes',
}, {
  symptom: 'sore_throat',
  value : 'no',
}, {
  symptom: 'chills',
  value : 'no'
}, {
  symptom: 'temperature',
  value : 101.2
}];

export const REPORTS_DATA = [{
  date: '3/3',
  report: '',
  daily_report: REPORT
}, {
  date: '4/3',
  report: '',
  daily_report: REPORT
}, {
  date: '5/3',
  report: '',
  daily_report: REPORT
}, {
  date: '6/3',
  report: '',
  daily_report: REPORT
}, {
  date: '7/3',
  report: '',
  daily_report: REPORT
}, {
  date: '8/3',
  report: '',
  daily_report: REPORT
}, {
  date: '9/3',
  report: '',
  daily_report: REPORT
}, {
  date: '10/3',
  report: false,
  daily_report: REPORT
}, {
  date: '11/3',
  report: false,
  daily_report: REPORT
}, {
  date: '12/3',
  report: false,
  daily_report: REPORT
}, {
  date: '13/3',
  report: false,
  daily_report: REPORT
}, {
  date: '14/3',
  report: false,
  daily_report: REPORT
}, {
  date: '15/3',
  report: true,
  daily_report: REPORT
}, {
  date: '16/3',
  report: true,
  daily_report: REPORT
}];

export const H_WORKER = [
  {
    first_name: 'Ashish',
    last_name: 'Ranjan',
    phone_no: '7579076350',
    whatsapp: '7579076350',
    emplyoee_id: '121',
    email: 'ashish@beehyv.com',
    hcw_type_id: '12',
    department: 'Software',
    action_required: 'test_ordered',
    reported_data: REPORTS_DATA

  }, {
    first_name: 'Ranvijay',
    last_name: 'Kumar',
    phone_no: '9790912111',
    whatsapp: '7231123212',
    emplyoee_id: '211',
    email: 'ranvijay@beehyv.com',
    hcw_type_id: '13',
    department: 'Software',
    action_required: 'results_pending',
    reported_data: REPORTS_DATA
  }, {

    first_name: 'Prasanna',
    last_name: '',
    phone_no: '0929109912',
    whatsapp: '0922121231',
    emplyoee_id: '13',
    email: 'prasanna@beehyv.com',
    hcw_type_id: '15',
    department: 'Admin',
    action_required: 'tested_positive',
    reported_data: REPORTS_DATA

  }, {
    first_name: 'Rishi',
    last_name: 'Jain',
    phone_no: '0922109912',
    whatsapp: '781121231',
    emplyoee_id: '78',
    email: 'rishi@beehyv.com',
    hcw_type_id: '16',
    department: 'Senior',
    action_required: 'tested_negative',
    reported_data: REPORTS_DATA
  }
];

export const ACTIONS = {
  'No action required' : 0,
  'Need to test': 1,
  'Test ordered': 2,
  'Results pending': 3,
  'Tested positive': 4,
  'Tested negative': 5
};

export const REPORTING = [
  {
    hcw: {
      id: 1,
      first_name: "hcw a",
      last_name: "l",
      is_active: true,
      phone_number: "1111111111",
      whatsapp_number: "1111111111",
      employee_id: null,
      email: null,
      department: "",
      hcw_type_id: 1,
      result_status_id: null
    },
    survey_list: [
      {
        id: 40,
        survey_url: "/survey/getForm?survey_id=40",
        survey_date: "2020-03-28T00:00:00Z",
        sent_time: "2020-03-28T09:01:03.873433Z",
        submitted_time: "2020-03-28T09:01:28.648665Z",
        survey_id: {
          id: 1,
          survey_name: "COVID-19"
        },
        result_id: {
          id: 2,
          result_status: "NEED TO TEST"
        }
      }
        ]}
]
