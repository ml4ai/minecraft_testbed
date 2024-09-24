import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExportTrialComponent } from './export-trial.component';

describe('ImportExportTrialComponent', () => {
  let component: ExportTrialComponent;
  let fixture: ComponentFixture<ExportTrialComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExportTrialComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExportTrialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
