import {Injectable} from '@angular/core';
import {ReportList} from './response';

@Injectable({
  providedIn: 'root'
})
export class HealthWorkerDialogService {
  private data: ReportList;

  constructor() {
  }

  setData(data: any) {
    this.data = data;
  }

  getData() {
    //cloning data to avoid changes
    if (this.data) {
      const data = JSON.parse(JSON.stringify(this.data));
      //resetting for subsequent add or update worker operations.
      this.data = null;
      return data;
    } else {
      return null;
    }

  }
}
