import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HealthWorkerDialogMobileComponent } from './health-worker-dialog-mobile.component';

describe('HealthWorkerDialogMobileComponent', () => {
  let component: HealthWorkerDialogMobileComponent;
  let fixture: ComponentFixture<HealthWorkerDialogMobileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HealthWorkerDialogMobileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HealthWorkerDialogMobileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
