import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentDialogComponent } from './experiment-dialog.component';

describe('ExperimentDialogComponent', () => {
  let component: ExperimentDialogComponent;
  let fixture: ComponentFixture<ExperimentDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExperimentDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExperimentDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
