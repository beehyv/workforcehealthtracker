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
