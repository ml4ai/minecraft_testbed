import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteTrialComponent } from './delete-trial.component';

describe('DeleteTrialComponent', () => {
  let component: DeleteTrialComponent;
  let fixture: ComponentFixture<DeleteTrialComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeleteTrialComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeleteTrialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
