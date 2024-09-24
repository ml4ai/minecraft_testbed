import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateReplayComponent } from './create-replay.component';

describe('CreateReplayComponent', () => {
  let component: CreateReplayComponent;
  let fixture: ComponentFixture<CreateReplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateReplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
