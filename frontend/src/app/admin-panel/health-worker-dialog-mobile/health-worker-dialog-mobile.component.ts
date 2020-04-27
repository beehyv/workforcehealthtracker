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
import {Router} from '@angular/router';
import {HealthWorkerDialogService} from '../../utils/health-worker-dialog.service';
import {ChronicIllness, FacilityList, HealthWorkerData, HwcType, ImmunoDeficiency, ReportList} from '../../utils/response';
import {CookieService} from 'ngx-cookie-service';
import {FormControl, Validators} from '@angular/forms';
import {ENGLISH_CONSTANT} from '../../utils/language/english';
import {dateRangeValidator} from '../../utils/dateRangeValidator';
import {FetchDataService} from '../../utils/fetch-data.service';
import {map, startWith} from 'rxjs/operators';
import {Observable} from 'rxjs';
import {DatePipe, Location} from '@angular/common';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-health-worker-dialog-mobile',
  templateUrl: './health-worker-dialog-mobile.component.html',
  styleUrls: ['./health-worker-dialog-mobile.component.scss']
})
export class HealthWorkerDialogMobileComponent implements OnInit {
  pageNumber = 1;
  isAddWorker = true;
  worker: ReportList;
  language = ENGLISH_CONSTANT;
  illnessCtrl = new FormControl();
  immunoCtrl = new FormControl();
  groupCtrl = new FormControl();
  emailFormControl = new FormControl('', [
    Validators.required,
    Validators.email,
  ]);
  nameControl = new FormControl('', [
    Validators.required,
    Validators.pattern('[a-zA-Z][^#&<>\\"~;$^%{}?]{1,20}$')
  ]);
  lastNameControl = new FormControl('', [
    Validators.pattern('[a-zA-Z][^#&<>\\"~;$^%{}?]{1,20}$')
  ]);
  phoneNumberControl = new FormControl('', [
    Validators.required,
    Validators.pattern('(\\+91(-)?|91(-)?|0(-)?)?[9876][0-9]{9}')
  ]);
  whatsAppNumberControl = new FormControl('', [
    Validators.pattern('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\\s\\./0-9]*$')
  ]);
  employeeIdControl = new FormControl('', [
    Validators.required,
  ]);
  hcwTypeIdControl = new FormControl('', [
    Validators.required
  ]);
  healthWorkerData: HealthWorkerData = new HealthWorkerData();
  minWorkerDOB: Date;
  maxWorkerDOB: Date;
  dateCtrl: FormControl;
  isMobileAndWhatsappSame = false;
  facilityLists: FacilityList[] = [];
  groups: any[] = [];
  chronicIllnesses: ChronicIllness[] = [];
  immuneDefeciency: ImmunoDeficiency[] = [];
  hwcLists: HwcType[] = [];
  filteredHWCtypes: Observable<HwcType[]>;
  isPhoneNotValid: boolean;
  private facilityData: any;

  constructor(private healthWorkerDialogService: HealthWorkerDialogService,
              private fetchDataService: FetchDataService,
              private cookieService: CookieService, private router: Router,
              private location: Location, private datePipe: DatePipe,
              private snackBar: MatSnackBar) {
  }

  ngOnInit(): void {
    const data = this.healthWorkerDialogService.getData();

    if (this.cookieService.get('isMobile') === 'false' || !data) {
      this.router.navigate(['/admin-panel']);
      return;
    }

    const today = new Date();
    (this.minWorkerDOB = new Date(today)).setFullYear(today.getFullYear() - 110);
    (this.maxWorkerDOB = new Date(today)).setFullYear(today.getFullYear() - 18);
    this.dateCtrl = new FormControl('', [
      Validators.required,
      dateRangeValidator(this.minWorkerDOB, this.maxWorkerDOB)
    ]);

    if (data.data) {
      this.illnessCtrl.setValue((data.data.chronic_illnesses ?? []).map(i => i.id));
      this.immunoCtrl.setValue((data.data.immunodeficiencies ?? []).map(i => i.id));
      this.groupCtrl.setValue((data.data.user_groups ?? []).map(i => i.id));
      this.healthWorkerData = data.data;
      this.hcwTypeIdControl.setValue(data.hwcData.hcw_type_name);
    }
    this.language = data.language;
    this.hwcLists = data.hcwList;
    this.facilityData = data.facilityData;
    this.isAddWorker = data.status === 'post';
    this.filteredHWCtypes = this.hcwTypeIdControl.valueChanges
      .pipe(
        startWith(''),
        map(HWCtype => HWCtype ? this._filterHWC_type(HWCtype) : this.hwcLists.slice())
      );
    this.getAllFacility();
    this.getAllChronicIllness();
    this.getAllImmunoDefeciency();
    this.getAllGroups();
  }

  getAllFacility() {
    this.fetchDataService.getAllFacility().subscribe((res) => {
      this.facilityLists = res;
    });
  }

  getAllChronicIllness() {
    this.fetchDataService.getAllChronicIllness().subscribe((res) => {
      this.chronicIllnesses = res;
    });
  }

  getAllImmunoDefeciency() {
    this.fetchDataService.getAllImmunoDefeciency().subscribe((res) => {
      this.immuneDefeciency = res;
    });
  }

  getAllGroups() {
    this.fetchDataService.getAllGroups().subscribe((res) => {
      this.groups = res;
    });
  }

  clearhcwTypeIdControl() {
    this.hcwTypeIdControl = new FormControl('', [
      Validators.required
    ]);
    this.filteredHWCtypes = this.hcwTypeIdControl.valueChanges
      .pipe(
        startWith(''),
        map(HWCtype => HWCtype ? this._filterHWC_type(HWCtype) : this.hwcLists.slice())
      );
  }

  checkForWhatsappNumber() {
    if (this.isMobileAndWhatsappSame) {
      this.healthWorkerData.whatsapp_number = this.healthWorkerData.phone_number;
    } else {
      this.healthWorkerData.whatsapp_number = '';
    }
  }

  saveHwc(hwcId) {
    this.healthWorkerData.hcw_type_id = hwcId;
  }

  cancel() {
    this.location.back();
  }

  submitDetails() {
    this.healthWorkerData.user_groups = this.groupCtrl.value;
    this.healthWorkerData.chronic_illnesses = this.illnessCtrl.value;
    this.healthWorkerData.immunodeficiencies = this.immunoCtrl.value;
    this.healthWorkerData.date_of_birth = this.datePipe.transform(this.dateCtrl.value, 'yyyy-MM-dd');
    // this.healthWorkerData.hcw_type_id = this.hcwTypeIdControl.value;
    this.healthWorkerData.facility_id = this.facilityData.id;

    if (!(this.nameControl.invalid || this.phoneNumberControl.invalid ||
      this.emailFormControl.invalid || this.employeeIdControl.invalid ||
      this.hcwTypeIdControl.invalid || !this.healthWorkerData.facility_id ||
      this.dateCtrl.invalid)) {
      // if (this.healthWorkerData.immunodeficiencies.length === 0) {
      //   this.healthWorkerData.immunodeficiencies.length = []
      // }
      if (this.isAddWorker) {
        this.fetchDataService.postHealthWorkerData(this.healthWorkerData).subscribe(_res => {
          this.snackBar.open(this.language.user_added_successfully, this.language.dismiss, {
            duration: 2000
          });
          return this.router.navigate(['/admin-panel']);
        }, (err) => {
          if (err.status === 201) {
            this.snackBar.open(this.language.worker_created_successfully, this.language.dismiss, {
              duration: 2000
            });
            return this.router.navigate(['/admin-panel']);
          } else if (err.status === 400) {
            this.snackBar.open(this.language.user_already_exist, this.language.dismiss, {
              duration: 4000
            });
          } else {
            this.snackBar.open(this.language.failure_message, this.language.dismiss, {
              duration: 2000
            });
            return this.router.navigate(['/admin-panel']);
          }
        });
      } else {
        this.fetchDataService.updateHealthWorkerData(this.healthWorkerData).subscribe(_res => {
          this.snackBar.open(this.language.user_added_successfully, this.language.dismiss, {
            duration: 2000
          });
          return this.router.navigate(['/admin-panel']);

        }, (err) => {
          if (err.status === 200) {
            this.snackBar.open(this.language.worker_updated, this.language.dismiss, {
              duration: 2000
            });
            return this.router.navigate(['/admin-panel']);
          } else if (err.status === 400) {
            this.snackBar.open(this.language.user_already_exist, this.language.dismiss, {
              duration: 4000
            });
          } else {
            this.snackBar.open(this.language.failure_message, this.language.dismiss, {
              duration: 2000
            });
            return this.router.navigate(['/admin-panel']);
          }
        });
      }
    } else if(this.nameControl.invalid){
      this.snackBar.open( this.language.invaild_name, this.language.dismiss, {
        duration: 2000
      });
    } else if(this.dateCtrl.invalid) {
      const dateOptions = {
        "year": "numeric",
        "month": "long",
        "day": "numeric"
      };
      this.snackBar.open( this.language.invalid_date1+this.minWorkerDOB.toLocaleDateString('en',dateOptions) + this.language.invalid_date2 +this.maxWorkerDOB.toLocaleDateString('en',dateOptions) + this.language.invalid_date3, this.language.dismiss, {
        duration: 2000
      });
    } else if (this.phoneNumberControl.invalid) {
      this.snackBar.open(this.language.invalid_number, this.language.dismiss, {
        duration: 2000
      });
    } else if(this.emailFormControl.invalid){
      this.snackBar.open( this.language.invalid_email, this.language.dismiss, {
        duration: 2000
      });
    } else if(this.employeeIdControl.invalid){
      this.snackBar.open( this.language.invalid_employee_id, this.language.dismiss, {
        duration: 2000
      });
    } else if(this.hcwTypeIdControl.invalid){
      this.snackBar.open( this.language.invalid_hcw_type_id, this.language.dismiss, {
        duration: 2000
      });
    } else {
      this.snackBar.open( this.language.fill_fields, this.language.dismiss, {
        duration: 2000
      });
    }
  }

  private _filterHWC_type(value: string): HwcType[] {
    const filterValue = value.toLowerCase();
    return this.hwcLists.filter(state => state.hcw_type_name.toLowerCase().indexOf(filterValue) === 0);
  }

  prevPage() {
    this.pageNumber--;
  }

  nextPage() {
    if(this.pageNumber === 1) {
      if (this.nameControl.invalid) {
        this.snackBar.open(this.language.invaild_name, this.language.dismiss, { duration: 2000 });
      }else if (this.dateCtrl.invalid) {
        const dateOptions = {
          "year": "numeric",
          "month": "long",
          "day": "numeric"
        };
        this.snackBar.open(this.language.invalid_date1 + this.minWorkerDOB.toLocaleDateString('en', dateOptions) +
          this.language.invalid_date2 + this.maxWorkerDOB.toLocaleDateString('en', dateOptions) + this.language.invalid_date3, this.language.dismiss,
          {duration: 2000});
      } else if (this.phoneNumberControl.invalid) {
        this.snackBar.open(this.language.invalid_number, this.language.dismiss, {duration: 2000});
      } else if (this.emailFormControl.invalid) {
        this.snackBar.open(this.language.invalid_email, this.language.dismiss, {duration: 2000});
      } else
        this.pageNumber++;
    } else {
      if (this.employeeIdControl.invalid) {
        this.snackBar.open(this.language.invalid_employee_id, this.language.dismiss, {duration: 2000});
      } else if (this.hcwTypeIdControl.invalid) {
        this.snackBar.open(this.language.invalid_hcw_type_id, this.language.dismiss, {duration: 2000});
      } else
        this.pageNumber++;
    }
  }
}
