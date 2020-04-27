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
import {CookieService} from 'ngx-cookie-service';
import {ENGLISH_CONSTANT} from './utils/language/english';
import {HINDI_CONSTANT} from './utils/language/hindi';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Workforce Health Tracker';
  cookieValue;
  isMobile = 'false';

  constructor(private router: Router, private cookieService: CookieService) {
    this.cookieValue = this.cookieService.get('language');
    if (!this.cookieValue) {
      this.changeLanguage('en');
    }
    if (window.innerWidth < 767) {
      cookieService.set('isMobile', 'true');
    } else {
      cookieService.set('isMobile', 'false');

    }
  }

  changeLanguage(language) {
    this.cookieService.set('language', language);
    this.cookieValue = this.cookieService.get('language');
    // if (!(this.router.url.indexOf('/en') || this.router.url.indexOf('/hi'))) {
    //   this.router.navigate([]).then(result => {
    //     window.open('#/' + this.router.url + '/' + language, '_self');
    //     window.location.reload();
    //   });
    // } else {
    //   const route = this.router.url.split('/')[1];
    //   const routeLang = this.router.url.split('/')[2];
    //   if ( routeLang !== language) {
    //     this.router.navigate([]).then(result => {
    //       window.open('#/' + route + '/' + language, '_self');
    //       window.location.reload();
    //     });
    //   }
    // }
    if (!this.cookieValue || this.cookieValue === language) {
      if (this.router.url.includes('survey')) {
        this.router.navigate([]).then(result => {
          window.location.reload();
        });
      }
    }
  }
}
