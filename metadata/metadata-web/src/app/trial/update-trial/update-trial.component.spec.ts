import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateTrialComponent } from './update-trial.component';

describe('UpdateTrialComponent', () => {
  let component: UpdateTrialComponent;
  let fixture: ComponentFixture<UpdateTrialComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UpdateTrialComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateTrialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
