import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {AdminPanelComponent} from './admin-panel/admin-panel.component';
import {LoginComponent} from './login/login.component';
import {SurveyComponent} from './survey/survey.component';
import {AuthGuard} from './auth.guard';
import {HealthWorkerDialogMobileComponent} from './admin-panel/health-worker-dialog-mobile/health-worker-dialog-mobile.component';


const routes: Routes = [
  {
    path: '',
    component: LoginComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'survey',
    component: SurveyComponent
  },
  {
    path: 'admin-panel',
    component: AdminPanelComponent,
    canActivate: [AuthGuard],
    children: [{
      path: 'en',
      component: AdminPanelComponent,
    }, {
      path: 'hi',
      component: AdminPanelComponent,
    }]
  },
  {
    path: 'addWorker',
    component: HealthWorkerDialogMobileComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'updateWorker',
    component: HealthWorkerDialogMobileComponent,
    canActivate: [AuthGuard]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
