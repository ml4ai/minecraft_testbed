import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RunReplayComponent } from './run-replay.component';

describe('RunReplayComponent', () => {
  let component: RunReplayComponent;
  let fixture: ComponentFixture<RunReplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RunReplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RunReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
