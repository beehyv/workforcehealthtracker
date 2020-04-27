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

import {Component, OnInit} from '@angular/core';
import {REPORT} from '../utils/constant';
import {HealthWorkerDialogComponent} from './health-worker-dialog/health-worker-dialog.component';
import {MatDialog} from '@angular/material/dialog';
import {
  HealthWorkerData,
  HwcType,
  PostStatus,
  ReportList,
  ResultStatus,
  SurveyList,
  GetReportList,
  Filter, GetAggregates
} from '../utils/response';
import {ENGLISH_CONSTANT} from '../utils/language/english';
import {HINDI_CONSTANT} from '../utils/language/hindi';
import {Router} from '@angular/router';
import {MatSnackBar} from '@angular/material/snack-bar';
import {CookieService} from 'ngx-cookie-service';
import {FetchDataService} from '../utils/fetch-data.service';
import {actions} from '../utils/actions';
import {HealthWorkerDialogService} from '../utils/health-worker-dialog.service';
import {FilterModalComponent} from './filter-modal/filter-modal.component';

export interface FilterList {
  name: string;
  id: string;
}
@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.scss']
})
export class AdminPanelComponent implements OnInit {
  search = "";
  reportResponse: GetReportList;
  hworkers: ReportList[];
  curretHWorkers: ReportList[];
  workerData: HealthWorkerData = new HealthWorkerData();
  actions: any[];
  actionsDictionary = {};
  colorsDictionary = {};
  surveyReport = ['Resend Survey', 'Fill the survey'];
  todayDate = new Date();
  startDate;
  report = REPORT;
  language = ENGLISH_CONSTANT;
  hwcLists: HwcType[] = [];
  userList: [];
  userListResponse: ReportList[];
  lang;
  dates: Date[] = [];
  resultStatus: ResultStatus[];
  postStatus: PostStatus = new PostStatus();
  isStatusDropdownChanged = false;
  problems: any[];
  facilityData;
  totalWorkers = 0; // TO-DO: later we will get it from the API
  pageIndex = 0;
  pageSize = 0;
  loadingReports = false;
  isMobile = "false";
  filters: any[];
  selectable = true;
  removable = true;
  groups = [];
  filterLists: FilterList[] = [];
  isFilter = false;
  filter: Filter = new Filter();
  searchOn = false;
  aggregatesValue: GetAggregates = new GetAggregates();
  constructor(public dialog: MatDialog, private router: Router,
              private snackBar: MatSnackBar, private cookieService: CookieService,
              private fetchDataService: FetchDataService,
              private healthWorkerDialogService: HealthWorkerDialogService) {
    this.isMobile = this.cookieService.get('isMobile');
    if (this.cookieService.get('language') === 'hi') {
      this.language = HINDI_CONSTANT;
    } else {
      this.language = ENGLISH_CONSTANT;
    }
    this.surveyReport = ['resend_survey', 'fill_survey'];
    this.actions = actions(this.language);
    this.problems = [{
      id: 1,
      question_text: this.language.cough,
    }, {
      id: 2,
      question_text: this.language.shortness_of_breath,
    }, {
      id: 3,
      question_text: this.language.temperature,
    }, {
      id: 4,
      question_text : this.language.foreign_travel_date
    }, {
      id: 5,
      question_text : this.language.cv_patient_contact_date
    }, {
      id: 6,
      question_text : this.language.any_cv_patient_contact
    }, {
      id: 7,
      question_text : this.language.any_foreign_travel
    }, {
      id: 8,
      question_text :  this.language.fever
    }, {
      id: 9,
      question_text:	this.language.immunodeficiency
    }
  ];
  }
  ngOnInit(): void {
    this.getResultStatus();
    this.dateArray();
    this.getReport();
    this.getAllHwcType();
    this.getFacilityByManager();
    this.getAllGroups();
    this.isFilter = JSON.parse(localStorage.getItem('is-filter'));
    // this.getAggregates();
  }

  openFilterDialog(): void {
    this.isFilter = !this.isFilter;
    localStorage.setItem('is-filter', JSON.stringify(this.isFilter));
    if(!this.isFilter) {
      this.closeFilter();
      return;
    }
    const dialogRef = this.dialog.open(FilterModalComponent, {
      data: {
        language: this.language,
        result_status: this.actions,
        groups: this.groups,
        isMobile: this.isMobile
      },
    });

    dialogRef.afterClosed().subscribe(result => {
      this.isFilter = false;
      if (result !== 'cancel' && result !== undefined) {
        this.filter = result;
        this.pageIndex = 0;
        this.isFilter = true;
        localStorage.setItem('filter-value', JSON.stringify(this.filter));
        this.changeToFilterList(this.filter);
        this.getReport();
      } else {
        this.isFilter = false;
      }
      localStorage.setItem('is-filter', JSON.stringify(this.isFilter));
    });
  }
  openHealthWorkerDialog(): void {
    const data = {
      language: this.language,
      hcwList: this.hwcLists,
      facilityData: this.facilityData,
      status: 'post'
    };
    if(this.isMobile === "true") {
      this.healthWorkerDialogService.setData(data);
      this.router.navigate(['/addWorker']);
      return;
    }
    const dialogRef = this.dialog.open(HealthWorkerDialogComponent, {
      panelClass: 'hwd-overlay-pane',
      id: 'health-worker-dialog',
      data: data,
    });

    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed');
      this.getAggregates();
      if (result === 'Successful') {
      this.getReport();
      }
    });
  }
  updateHealthWorkerDialog(h_worker): void {
    const data = {
      data: h_worker,
      language: this.language,
      hcwList: this.hwcLists,
      facilityData: this.facilityData,
      status: 'update',
      hwcData: this.hwcLists.filter(hcwdata => hcwdata.id === h_worker.hcw_type_id)[0],
      chronicIllness: h_worker.chronic_illnesses
    };
    if(this.isMobile === 'true') {
      this.healthWorkerDialogService.setData(data);
      this.router.navigate(['/updateWorker']);
      return;
    }
    const dialogRef = this.dialog.open(HealthWorkerDialogComponent, {
      panelClass: 'hwd-overlay-pane',
      id: 'health-worker-dialog',
      data: data,
    });

    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed');
      // always need to refresh
      this.getReport();
    });
  }
  takeSurvey(action , phone_number) {
    if (action === 'fill_survey') {
      this.fetchDataService.generateSurvey(phone_number).subscribe( (res) => {
        localStorage.setItem('survey-url', res.split('=')[1]);
        this.router.navigate([]).then(_result => {
          window.open('#/survey', '_blank');
        });
      }, (res) => {
        localStorage.setItem('survey-url', res.error.text.split('=')[1]);
        this.router.navigate([]).then(_result => {
          window.open('#/survey', '_blank');
        });
      });
    } else {
      this.loadingReports = true;
      this.fetchDataService.sendWhatsAPP(phone_number).subscribe(() => {
        this.loadingReports = false;
        this.snackBar.open('Survey Sent', 'dismiss', {
          duration: 2000
        });
      });
    }
  }

  checkAge(worker) {
    return 1960 > worker;
  }

  private updateWorkerList(reportData: GetReportList) {
    if (!this.pageSize){
      this.pageSize = reportData.results.length;
    }
    this.totalWorkers = reportData.count;
    this.hworkers = reportData.results;
    this.userListResponse = reportData.results;
  }
  getReport() {
    this.loadingReports = true;
    this.getAggregates();
    let filter: any = {};
    if(localStorage.getItem('filter-value')){
      this.groups = JSON.parse(localStorage.getItem('groups'));
      filter = JSON.parse(localStorage.getItem('filter-value'));
      this.changeToFilterList(filter);
    }
    filter.pageIndex = this.pageIndex + 1;
    this.fetchDataService.getReport(filter).subscribe(reportData => {
      this.updateWorkerList(reportData);
      this.loadingReports = false;
    });
  }
  logout() {
    localStorage.clear();
    this.router.navigate(['login']);
  }
  getAllHwcType() {
    this.fetchDataService.getAllHwcType().subscribe( (res) => {
      this.hwcLists = res;
      console.log(this.hwcLists);
    });
  }
  searchUser(text) {
    let inputString = text.target.value;
    this.hworkers = [];
    inputString = inputString.trim().toLowerCase();
    if (inputString === '') {
      this.hworkers = this.userListResponse;
    } else {
      for (let i = 0; i < this.userListResponse.length; i++) {
        for ( const key in this.userListResponse[i]) {
          if (this.userListResponse[i][key] !== undefined && this.userListResponse[i][key] !== null) {
            for ( const  key2 in this.userListResponse[i][key]) {
              if (String(this.userListResponse[i][key][key2]).toLowerCase().indexOf(inputString) !== -1) {
                this.hworkers.push(this.userListResponse[i]);
                break;
              }
            }
          }
        }
      }
    }
  }
  dateArray(){
    this.startDate = new Date(this.todayDate.setDate(this.todayDate.getDate() - 14));
    for (let i = 14; i > 0 ; i--){
      this.dates.push(new Date(this.startDate.setDate(this.startDate.getDate() + 1)));
    }
  }
  sortByDate(hWorker: SurveyList[], submittedDate) {
      for (let hw of hWorker) {
          let surveyListDate = hw.survey_instance.submitted_time?.split('-')[2].split('T')[0] + '/' + hw.survey_instance.submitted_time?.split('-')[1];
          if (surveyListDate === submittedDate) {
            return hw.survey_instance?.result_id?.id === 2;
          }

      }
      return null;
  }
  getAllGroups() {
    this.fetchDataService.getAllGroups().subscribe( (res) => {
      localStorage.setItem('groups', JSON.stringify(res));
      this.groups = res;
    });
  }
  getResultStatus() {
    this.fetchDataService.getResultStatus().subscribe( (res) =>{
      this.resultStatus = res;
      res.forEach((value) => {
        if (value.id === 1) {
          this.actionsDictionary[value.id] = this.language.no_action
          this.colorsDictionary[value.id] = "#444444"
        } else if (value.id === 3) {
          this.actionsDictionary[value.id] = this.language.results_pending
          this.colorsDictionary[value.id] = "#444444"
        } else if (value.id === 6) {
          this.actionsDictionary[value.id] = this.language.test_ordered
          this.colorsDictionary[value.id] = "#444444"
        } else if (value.id === 4) {
          this.actionsDictionary[value.id] = this.language.tested_negative
          this.colorsDictionary[value.id] = "#e60000"
        } else if (value.id === 5) {
          this.actionsDictionary[value.id] = this.language.tested_positive
          this.colorsDictionary[value.id] = "#4cbb17"
        } else if (value.id === 7) {
          this.actionsDictionary[value.id] = this.language.home_quarantine_symptom
          this.colorsDictionary[value.id] = "#f76a14"
        } else if (value.id === 8) {
          this.actionsDictionary[value.id] = this.language.precaution_measure_symptom
          this.colorsDictionary[value.id] = "#ffb366"
        } else if (value.id === 9) {
          this.actionsDictionary[value.id] = this.language.home_quarantine_general
          this.colorsDictionary[value.id] = "#ffb366"
        } else if (value.id === 10) {
          this.actionsDictionary[value.id] = this.language.precaution_measure_general
          this.colorsDictionary[value.id] = "#ffb366"
        }else if (value.id === 11) {
          this.actionsDictionary[value.id] = this.language.advise_to_stay_home
          this.colorsDictionary[value.id] = "#ffb366"
        }
      });
    });
  }

  searchClicked() {
    if (!this.searchOn) {
      this.searchOn = true;
      return
    }
    this.searchReports()
  }

  searchReports(pageIndex = 0) {
    this.pageIndex = 0;
    this.isFilter = true;
    let filters= localStorage.getItem('filter-value');
    if(filters)
      this.filter = JSON.parse(filters);

    this.filter.search_name = this.search;
    localStorage.setItem('filter-value', JSON.stringify(this.filter));
    this.changeToFilterList(this.filter);
    localStorage.setItem('is-filter', JSON.stringify(this.isFilter));
    this.getReport();
    this.searchOn = false;
  }

  setFontColor(id) {
    var style = {"color": this.colorsDictionary[id]}
    return style;
  }

  applyStyle(id) {
    if (id === null) {
      var style = {"border-left": "8px solid grey"}
      return style;
    }
    var style = {"border-left": "8px solid "+ this.colorsDictionary[id] +""}
    return style;
  }

  saveStatus(statusId, phoneNo, index) {
    this.getAggregates();
    this.isStatusDropdownChanged = true
    this.postStatus.status_id = this.actions[statusId].id;
    this.postStatus.phone_number = phoneNo;
    this.hworkers[index].hcw.result_status_id = this.actions[statusId].id;
    if (statusId === 0) {
      this.hworkers[index].hcw.result_status_id = null;
    }

    this.fetchDataService.postStatus(this.postStatus).subscribe(() => {
      console.log(document.getElementById('status_change'));
      this.getReport();
    }, () => {
      this.getReport();
    });
  }

  getFacilityByManager() {
    this.fetchDataService.getfaciltityByManager().subscribe( (res) => {
      this.facilityData = res;
    });
  }

  onPageChange(event) {
    this.pageIndex = event.pageIndex;
    this.getReport();
  }

  getAgeFromDOB(date_of_birth: string) {
    return this.todayDate.getFullYear() - +date_of_birth.split('-')[0];
  }

  getStatusMessage(result_status_id: number) {
    if (result_status_id === null) {
      result_status_id = 1;
    }
    const action = this.actions.filter(action=>action.id === result_status_id)[0];
    return action.result_message;
  }
  changeToFilterList(filter: Filter) {
    this.filterLists = [];
    for (var key in filter) {
      if( key === 'group'){
        filter.group = filter?.group?.replace(/,\s*$/, "");
        let groupLength = filter.group?.split(',') ? filter.group?.split(',').length : 0;
        for (let i = 0; i < groupLength; i++) {
          if (filter[key]) {
            this.filterLists.push({id: key, name: this.groups.filter(action => action.id === +filter.group.split(',')[i])[0].name});
          }
        }
      } else if ( key === 'result_status' ){
        if (filter[key]) {
          this.filterLists.push({id: key, name: this.actions.filter(action => action.id === filter.result_status)[0].result_status});
        }
      } else if( key != 'pageIndex'){
        if (filter[key]) {
          this.filterLists.push({id: key, name: key + " - " + filter[key]});
        }
      }
    }
  }

  remove(filterList: FilterList): void {
    const index = this.filterLists.indexOf(filterList);
    if (index >= 0) {
      this.filterLists.splice(index, 1);
    }
    if (filterList.id === 'search_name')
      this.search = '';
    this.reCallReportFromFilter(this.filterLists);
    // console.log(this.filterLists);
  }
  closeFilter() {
    this.search = '';
    this.filter = new Filter();
    this.pageIndex = 0;
    localStorage.removeItem('filter-value');
    this.getReport();
  }
  reCallReportFromFilter(filterList: FilterList[]) {
    this.filter = new Filter();
    this.pageIndex = 0;
    this.filter.group = '';
    for(let item of filterList) {
      if(item.id === 'group') {
         this.filter.group += this.groups.filter(groupVal => groupVal.name === item.name)[0].id + ',';
      }
      else if(item.id === 'result_status') {
        this.filter.result_status = this.actions.filter(action => action.result_status === item.name)[0].id;
      }
      else if (item.id === 'isChronicIllness' ){
        this.filter.isChronicIllness = item.name.split('-')[1].trim();
      }
      else if ( item.id === 'isImmunodeficiency' ){
        this.filter.isImmunodeficiency = item.name.split('-')[1].trim();
      }
      else if (item.id === 'min_age' ){
        this.filter.min_age = +item.name.split('-')[1].trim();
      }
      else if ( item.id === 'max_age'){
        this.filter.max_age = +item.name.split('-')[1].trim();
      }else if ( item.id === 'search_name'){
        this.filter.search_name = item.name.split('-')[1].trim();
      }
    }
    localStorage.setItem('filter-value', JSON.stringify(this.filter));
    if(this.filterLists.length === 0) {
      this.filter = new Filter();
      this.pageIndex = 0;
      this.isFilter = false;
      localStorage.setItem('is-filter', JSON.stringify(false));
    }
    this.getReport();
  }
  getAggregates() {
    this.fetchDataService.getAggregates().subscribe( (res) =>{
      this.aggregatesValue = res;
    });
  }
}

