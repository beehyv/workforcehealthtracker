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
