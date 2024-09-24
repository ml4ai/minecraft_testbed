import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HumanAdvisorComponent } from './human-advisor.component';

describe('HumanAdvisorComponent', () => {
  let component: HumanAdvisorComponent;
  let fixture: ComponentFixture<HumanAdvisorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HumanAdvisorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HumanAdvisorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
