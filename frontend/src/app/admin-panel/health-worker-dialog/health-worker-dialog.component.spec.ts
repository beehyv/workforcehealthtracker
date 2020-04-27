import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HealthWorkerDialogComponent } from './health-worker-dialog.component';

describe('HealthWorkerDialogComponent', () => {
  let component: HealthWorkerDialogComponent;
  let fixture: ComponentFixture<HealthWorkerDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HealthWorkerDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HealthWorkerDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
