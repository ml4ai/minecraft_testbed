import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateReplayComponent } from './update-replay.component';

describe('UpdateReplayComponent', () => {
  let component: UpdateReplayComponent;
  let fixture: ComponentFixture<UpdateReplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UpdateReplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
