import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportTrialComponent } from './import-trial.component';

describe('ImportTrialComponent', () => {
  let component: ImportTrialComponent;
  let fixture: ComponentFixture<ImportTrialComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ImportTrialComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImportTrialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
