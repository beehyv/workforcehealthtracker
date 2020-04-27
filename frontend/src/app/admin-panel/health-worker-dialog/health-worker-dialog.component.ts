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

import {Component, Inject, OnInit} from '@angular/core';
import {AbstractControl, FormControl, ValidationErrors, ValidatorFn, Validators} from '@angular/forms';
import {ChronicIllness, FacilityList, HealthWorkerData, HwcType, ImmunoDeficiency} from '../../utils/response';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {FetchDataService} from '../../utils/fetch-data.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {map, startWith} from 'rxjs/operators';
import {Observable} from 'rxjs';
import {DatePipe} from '@angular/common';
import {ENGLISH_CONSTANT} from '../../utils/language/english';
import {dateRangeValidator} from '../../utils/dateRangeValidator';

@Component({
  selector: 'app-health-worker-dialog',
  templateUrl: './health-worker-dialog.component.html',
  styleUrls: ['./health-worker-dialog.component.scss']
})
export class HealthWorkerDialogComponent implements OnInit {
  minWorkerDOB: Date;
  maxWorkerDOB: Date;
  isEnglish;
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
  hcwTypeIdControl = new FormControl( '', [
    Validators.required
  ]);
  dateCtrl;
  groups = [];
  groupCtrl = new FormControl();
  illnessCtrl = new FormControl();
  immunoCtrl = new FormControl();
  language = ENGLISH_CONSTANT;
  facilityLists: FacilityList[] = [];
  hwcLists: HwcType[] = [];
  healthWorkerData: HealthWorkerData = new HealthWorkerData();
  disableBoolean;
  filteredHWCtypes: Observable<HwcType[]>;
  facilityData;
  status;
  chronicIllnesses: ChronicIllness[] = [];
  immuneDefeciency: ImmunoDeficiency[] = [];
  isMobileAndWhatsappSame: boolean;
  isPhoneNotValid: boolean;
  constructor(private dialogRef: MatDialogRef<HealthWorkerDialogComponent>,
              @Inject(MAT_DIALOG_DATA) data, private fetchDataService: FetchDataService,
              private snackBar: MatSnackBar, private datepipe: DatePipe) {
    if (data.data) {
      this.healthWorkerData.user_groups = this.getIdOfGroups(data.data.user_groups ?? []);
      this.healthWorkerData.chronic_illnesses = this.getIdOfChronicDisease(data.data.chronic_illnesses ?? []);
      this.healthWorkerData.immunodeficiencies = this.getIdOfImmunoDeficiency(data.data.immunodeficiencies ?? []);
      this.illnessCtrl.setValue(this.getIdOfChronicDisease(data.data.chronic_illnesses ?? []));
      this.immunoCtrl.setValue(this.getIdOfChronicDisease(data.data.immunodeficiencies ?? []));
      this.groupCtrl.setValue(this.getIdOfGroups(data.data.user_groups ?? []))
      this.healthWorkerData = data.data;
      this.hcwTypeIdControl.setValue(data.hwcData?.hcw_type_name);
    }
    this.language = data.language;
    this.hwcLists = data.hcwList;
    this.facilityData = data.facilityData;
    this.status = data.status;
    this.filteredHWCtypes = this.hcwTypeIdControl.valueChanges
      .pipe(
        startWith(''),
        map(HWCtype => HWCtype ? this._filterHWC_type(HWCtype) : this.hwcLists.slice())
      );
  }
  private _filterHWC_type(value: string): HwcType[] {
    const filterValue = value.toLowerCase();

    return this.hwcLists.filter(state => state.hcw_type_name.toLowerCase().indexOf(filterValue) === 0);
  }
  ngOnInit(): void {
    const today = new Date();
    (this.minWorkerDOB = new Date(today)).setFullYear(today.getFullYear() - 110);
    (this.maxWorkerDOB = new Date(today)).setFullYear(today.getFullYear() - 18);
    this.dateCtrl = new FormControl('', [
      Validators.required,
      dateRangeValidator(this.minWorkerDOB,this.maxWorkerDOB)
    ]);
    this.getAllFacility();
    this.getAllChronicIllness();
    this.getAllImmunoDefeciency();
    this.getAllGroups();
  }
  submitDetails() {
    this.healthWorkerData.user_groups = this.groupCtrl.value;
    this.healthWorkerData.chronic_illnesses = this.illnessCtrl.value;
    this.healthWorkerData.immunodeficiencies = this.immunoCtrl.value;
    this.healthWorkerData.date_of_birth = this.datepipe.transform(this.dateCtrl.value, 'yyyy-MM-dd');
    // this.healthWorkerData.hcw_type_id = this.hcwTypeIdControl.value;
    this.healthWorkerData.facility_id = this.facilityData.id;

    if (!(this.nameControl.invalid || this.phoneNumberControl.invalid ||
      this.emailFormControl.invalid || this.employeeIdControl.invalid ||
      this.hcwTypeIdControl.invalid || !this.healthWorkerData.facility_id ||
      this.dateCtrl.invalid )) {
        // if (this.healthWorkerData.immunodeficiencies.length === 0) {
        //   this.healthWorkerData.immunodeficiencies.length = []
        // }
      if ( this.status === 'post') {
        this.fetchDataService.postHealthWorkerData(this.healthWorkerData).subscribe((res) => {
          this.snackBar.open(this.language.user_added_successfully, this.language.dismiss, {
            duration: 2000
          });
          this.dialogRef.close('Successful');

        }, (err) => {
          if(err.status === 201) {
            this.snackBar.open(this.language.worker_created_successfully, this.language.dismiss, {
              duration: 2000
            });
            this.dialogRef.close('Successful');
          } else if( err.status === 400) {
            this.snackBar.open( this.language.user_already_exist, this.language.dismiss, {
              duration: 4000
            });
          } else {
            this.snackBar.open(this.language.failure_message, this.language.dismiss, {
              duration: 2000
            });
            this.dialogRef.close('Successful');
          }
        });
      } else {
        this.fetchDataService.updateHealthWorkerData(this.healthWorkerData).subscribe((res) => {
          this.snackBar.open(this.language.user_added_successfully, this.language.dismiss, {
            duration: 2000
          });
          this.dialogRef.close('Successful');

        }, (err) => {
          if(err.status === 200) {
            this.snackBar.open(this.language.worker_updated, this.language.dismiss, {
              duration: 2000
            });
            this.dialogRef.close('Successful');
          } else if (err.status === 400) {
            this.snackBar.open(this.language.user_already_exist, this.language.dismiss, {
              duration: 4000
            });
          } else {
            this.snackBar.open(this.language.failure_message, this.language.dismiss, {
              duration: 2000
            });
            this.dialogRef.close('Successful');
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

  cancel() {
    this.dialogRef.close();
  }
  getAllFacility() {
    this.fetchDataService.getAllFacility().subscribe( (res) => {
      this.facilityLists = res;
    });
  }

  saveHwc(hwcId) {
    this.healthWorkerData.hcw_type_id = hwcId;
  }
  getAllChronicIllness() {
    this.fetchDataService.getAllChronicIllness().subscribe( (res) => {
      this.chronicIllnesses = res;
    });
  }

  getAllImmunoDefeciency() {
    this.fetchDataService.getAllImmunoDefeciency().subscribe( (res) => {
      this.immuneDefeciency = res;
    });
  }

  getAllGroups() {
    this.fetchDataService.getAllGroups().subscribe( (res) => {
      this.groups = res;
    });
  }

  getIdOfChronicDisease(chronicIllnesses) {
    const chronic = [];
    for ( const chronicIllness of chronicIllnesses){
      chronic.push(chronicIllness.id);
    }
    return chronic;
  }

  getIdOfGroups(groupsObj) {
    const group = [];
    for ( const g of groupsObj){
      group.push(g.id);
    }
    return group;
  }


  checkForWhatsappNumber() {
    if (this.isMobileAndWhatsappSame) {
      this.healthWorkerData.whatsapp_number = this.healthWorkerData.phone_number;
    }
  }

  private getIdOfImmunoDeficiency(immunoDeficiencies) {
    const deficiencies = [];
    for ( const immunoDeficiency of immunoDeficiencies){
      deficiencies.push(immunoDeficiency.id);
    }
    return deficiencies;
  }

  clearhcwTypeIdControl() {
    this.hcwTypeIdControl =  new FormControl( '', [
      Validators.required
    ]);
    this.filteredHWCtypes = this.hcwTypeIdControl.valueChanges
      .pipe(
        startWith(''),
        map(HWCtype => HWCtype ? this._filterHWC_type(HWCtype) : this.hwcLists.slice())
      );
  }
}
