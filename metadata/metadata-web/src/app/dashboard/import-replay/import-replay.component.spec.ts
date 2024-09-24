import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportReplayComponent } from './import-replay.component';

describe('ImportReplayComponent', () => {
  let component: ImportReplayComponent;
  let fixture: ComponentFixture<ImportReplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ImportReplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImportReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
