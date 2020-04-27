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
import {FetchDataService} from '../utils/fetch-data.service';
import {ActivatedRoute, Router} from '@angular/router';
import {ENGLISH_CONSTANT} from '../utils/language/english';
import {HINDI_CONSTANT} from '../utils/language/hindi';
import {MatSnackBar} from '@angular/material/snack-bar';
import {CookieService} from 'ngx-cookie-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  username: string = null;
  password: string = null;
  language = ENGLISH_CONSTANT;
  formLanguage = 'ENGLISH';
  showLoader = false;

  constructor(private fetchDataService: FetchDataService,
              private router: Router,
              private route: ActivatedRoute,
              private snackbar: MatSnackBar,
              private cookieService: CookieService) { }

  ngOnInit(): void {
    if (this.cookieService.get('language') === 'hi') {
      this.language = HINDI_CONSTANT;
    } else {
      this.language = ENGLISH_CONSTANT;
    }
  }

  login() {
    this.showLoader = true;
    this.fetchDataService.login(this.username, this.password, (response) => {
      this.showLoader = false;
      const body = response.body;
      if (body['token']) {
        localStorage.setItem('authToken', body['token']);
        this.router.navigate(['/admin-panel'], {relativeTo: this.route});
      } else {

      }
    }, () => {
      this.showLoader = false;
      this.snackbar.open(this.language.invalid_credential, 'Close', {duration: 5000});
    });
  }
}
