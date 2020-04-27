import { TestBed } from '@angular/core/testing';

import { HealthWorkerDialogService } from './health-worker-dialog.service';

describe('HealthWorkerDialogService', () => {
  let service: HealthWorkerDialogService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(HealthWorkerDialogService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
