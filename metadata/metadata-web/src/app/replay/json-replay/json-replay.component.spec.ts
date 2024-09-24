import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JsonReplayComponent } from './json-replay.component';

describe('JsonReplayComponent', () => {
  let component: JsonReplayComponent;
  let fixture: ComponentFixture<JsonReplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JsonReplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JsonReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
