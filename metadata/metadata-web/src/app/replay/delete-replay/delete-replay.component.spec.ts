import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteReplayComponent } from './delete-replay.component';

describe('DeleteReplayComponent', () => {
  let component: DeleteReplayComponent;
  let fixture: ComponentFixture<DeleteReplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeleteReplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeleteReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
