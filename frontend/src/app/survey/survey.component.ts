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

import { Component, OnInit } from '@angular/core';
import {HINDI_CONSTANT} from '../utils/language/hindi';
import {ENGLISH_CONSTANT} from '../utils/language/english';
import {FetchDataService} from '../utils/fetch-data.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Question} from '../utils/surveyResponseModel';
import {MatSnackBar} from '@angular/material/snack-bar';
import {CookieService} from 'ngx-cookie-service';
import {SurveyQuestions} from '../utils/response';
import { DatePipe } from '@angular/common';
import {FormControl, Validators} from '@angular/forms';
import {dateRangeValidator} from '../utils/dateRangeValidator';

@Component({
  selector: 'app-survey',
  templateUrl: './survey.component.html',
  styleUrls: ['./survey.component.scss']
})
export class SurveyComponent implements OnInit {
  oldestDateAllowed = new Date(0);
  today = new Date();
  foreignTravelDateCtrl;
  coronaPatientHistoryDateCtrl;
  booleans: Boolean[] = new Array(SurveyQuestions.length);
  temperature = null;
  hasChills = null;
  hasCough = null;
  hasShortedNessOfBreadth = null;
  // hasSoreThroat = null;
  hasFever = null;
  // hasImmunodeficiency = null;
  hasForeignTravel = null;
  foreignTravelDate: Date = null;
  hasCoronaPatientHistory = null;
  coronaPatientHistoryDate: Date = null;
  survey_worker_name: string;
  surveyId = null;
  survey_date: string;
  surveyForm: SurveyQuestions[];
  // surveyQuestions: SurveyQuestions[];
  loadingSurvey = false;
  surveyMapping = [
    {question_id: 1, key: 1},
    {question_id: 2, key: 2},
    {question_id: 5, key: 3},
    {question_id: 6, key: 4},
    {question_id: 7, key: 5},
    {question_id: 8, key: 6},
    {question_id: 9, key: 7},
    {question_id: 10, key: 8},
    {question_id: 11, key: 9},
    {question_id: 12, key: 10},
  ];
  language = ENGLISH_CONSTANT;
  alreadySubmitted: boolean = false;
  submittedSuccessfully: boolean = false;
  formLanguage = 'ENGLISH';
  showOTPscreen = true;
  userDetail: any;
  isTandCChecked: boolean;
  otpValue: string;
  constructor(private fetchDataService: FetchDataService,
              private router: Router,
              private route: ActivatedRoute,
              private snackbar: MatSnackBar,
              private cookieService: CookieService,
              private datePipe: DatePipe) {
    if (localStorage.getItem('authToken')) {
      this.showOTPscreen = false;
    }
  }

  ngOnInit(): void {
    this.loadingSurvey = true;
    this.foreignTravelDateCtrl = new FormControl('', [
      Validators.required,
      dateRangeValidator(this.oldestDateAllowed, this.today)
    ]);
    this.coronaPatientHistoryDateCtrl = new FormControl('', [
      Validators.required,
      dateRangeValidator(this.oldestDateAllowed, this.today)
    ]);
    if (this.cookieService.get('language') === 'hi') {
      this.language = HINDI_CONSTANT;
    } else {
      this.language = ENGLISH_CONSTANT;
    }
    this.route.queryParams.subscribe(params => {
      if ( !params.survey_id){
        this.surveyId = localStorage.getItem('survey-url');
        // this.surveyId = 88;
      } else {
        this.surveyId = params.survey_id;
        localStorage.setItem('survey-id', this.surveyId);
      }
      if (localStorage.getItem('authToken') || localStorage.getItem('not-of-otp-screen')) {
        this.showOTPscreen = false;
        if (localStorage.getItem('survey-id')) {
          this.surveyId = localStorage.getItem('survey-id');
        }
        this.fetchDataService.getSurveyForm(this.surveyId).subscribe((response) => {
          // this.surveyQuestions = response['questions'];
          this.loadingSurvey = false;
          this.survey_worker_name = response['username'];
          this.survey_date = response['survey_date'];
          this.surveyForm = response['questions'];
        }, (error) => {
         this.getOTPValue();
        });
      } else {
        if (!this.surveyId) {
          this.surveyId = localStorage.getItem('survey-id');
          this.getOTPValue();
        } else {
            this.getOTPValue();
          }
        }
    });
  }

  generateSurveyResponse() {
    const response: Question[] = [];
    for (const question of this.surveyForm) {
      response.push(new Question(question.id, this.getResponseOfQuestion(question.id), this.surveyId));
    }
    return response;
  }

  getResponseOfQuestion(questionId) {
    const mapping = this.surveyMapping.filter((item) => {
      if (item.question_id === questionId) {
        return true;
      } else {
        return false;
      }
    });
    if (mapping.length === 0) {
      return null;
    } else {
      switch (mapping[0].key) {
        case 1:
          return this.hasCough;
          break;
        case 2:
          return this.hasShortedNessOfBreadth;
          break;
        // case 3:
        //   return this.hasSoreThroat;
        //   break;
        case 8:
          return this.hasFever;
          break;
        case 3:
          return (this.temperature === null || this.temperature === '') ? "" : this.temperature;
          break;
        case 6:
          return this.hasCoronaPatientHistory;
          break;
        case 5:
          return this.coronaPatientHistoryDate === null ? "" : this.datePipe.transform(this.coronaPatientHistoryDate, 'yyyy-MM-dd');
          break;
        case 7:
          return this.hasForeignTravel;
          break;
        case 4:
          return this.foreignTravelDate === null ? "" : this.datePipe.transform(this.foreignTravelDate, 'yyyy-MM-dd');
          break;
        // case 9:
        //   return this.hasImmunodeficiency;
        //   break;
      }
    }
  }

  isFormComplete() {

    if ((this.hasCough !== null)
      && (this.hasShortedNessOfBreadth !== null)
      && (this.hasFever !== null && (this.hasFever === true ? (this.temperature !== null && this.temperature > '94' && this.temperature < '106') : true))
      && (this.hasCoronaPatientHistory !== null && (this.hasCoronaPatientHistory === true ? this.coronaPatientHistoryDate !== null : true))
      && (this.hasForeignTravel !== null && (this.hasForeignTravel === true ? this.foreignTravelDate !== null : true))
      // && (this.hasImmunodeficiency !== null)
    ) {
      return true;
    } else {
      return false;
    }
  }

  submit() {
    // const surveyData = {
    //   cough: this.hasCough,
    //   shortness_of_breath: this.hasShortedNessOfBreadth,
    //   sore_throat: this.hasSoreThroat,
    //   chills: this.hasChills,
    //   temperature: this.temperature,
    //   survey_id: this.surveyId
    // };
    this.coronaPatientHistoryDate;
    if ((this.hasForeignTravel && this.foreignTravelDateCtrl.invalid) || (this.hasCoronaPatientHistory && this.coronaPatientHistoryDateCtrl.invalid)) {
      return this.snackbar.open(this.language.invalid_date, this.language.dismiss, {duration: 1000});
    }
    if (this.isFormComplete()) {
      this.loadingSurvey = true;
      const surveyData = this.generateSurveyResponse();
      this.fetchDataService.postSurveyData(surveyData, (response) => {
        this.loadingSurvey = false;
        this.snackbar.open(this.language.success_message, this.language.dismiss, {duration: 1000});
        this.submittedSuccessfully = true;
        localStorage.removeItem('not-of-otp-screen');
        localStorage.removeItem('survey-id');
        setTimeout(function() {
          var win = window.open("about:blank", "_self");
          win.close();
        }, 3000);
      }, () => {
        this.snackbar.open(this.language.failure_message, this.language.dismiss, {duration: 1000});
        this.alreadySubmitted = true;
        setTimeout(function() {
          var win = window.open("about:blank", "_self");
          win.close();
        }, 3000);
      });
    } else if (this.hasFever !== null && (this.hasFever === true ? (this.temperature !== null && (this.temperature < '95' || this.temperature > '105')) : false)) {
      this.snackbar.open(this.language.invalid_temperature, this.language.dismiss, {duration: 1000});
    } else {
      this.snackbar.open(this.language.please_fill_all_field, this.language.dismiss, {duration: 1000});
    }
  }
  submitForOTP() {
    if (this.isTandCChecked || this.userDetail.consent) {
      this.fetchDataService.verifyOTP(this.surveyId, this.otpValue).subscribe( (res) => {
        console.log(res);
        if (res['verified']){
          this.fetchDataService.getSurveyForm(this.surveyId).subscribe((response) => {
            this.showOTPscreen = false;
            localStorage.setItem('not-of-otp-screen', 'true');
            // this.surveyQuestions = response['questions'];
            this.survey_worker_name = response['username'];
            this.survey_date = response['survey_date'];
            this.surveyForm = response['questions'];
          });
        } else {
          this.snackbar.open(this.language.failure_otp_message, this.language.dismiss, {duration: 1000});
        }
      });
    } else {
      alert(this.language.read_T_C);
    }
  }
  resendOTP() {

    this.fetchDataService.getResendOTP(this.surveyId).subscribe((response) => {
      console.log(response);
    });
  }
  getOTPValue() {
    this.fetchDataService.getOTPScreen(this.surveyId).subscribe((response) => {
      this.loadingSurvey = false;
      console.log(response);
      this.userDetail = response;
    });
  }
}
