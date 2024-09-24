import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MissionRunnerComponent } from './mission-runner.component';

describe('MussionRunnerComponent', () => {
  let component: MissionRunnerComponent;
  let fixture: ComponentFixture<MissionRunnerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MissionRunnerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MissionRunnerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
