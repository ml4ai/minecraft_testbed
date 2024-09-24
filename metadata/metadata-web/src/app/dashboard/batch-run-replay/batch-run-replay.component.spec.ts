import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BatchRunReplayComponent } from './batch-run-replay.component';

describe('BatchRunReplayComponent', () => {
  let component: BatchRunReplayComponent;
  let fixture: ComponentFixture<BatchRunReplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BatchRunReplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BatchRunReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
