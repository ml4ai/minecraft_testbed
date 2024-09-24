import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExportReplayComponent } from './export-replay.component';

describe('ExportReplayComponent', () => {
  let component: ExportReplayComponent;
  let fixture: ComponentFixture<ExportReplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExportReplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExportReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
