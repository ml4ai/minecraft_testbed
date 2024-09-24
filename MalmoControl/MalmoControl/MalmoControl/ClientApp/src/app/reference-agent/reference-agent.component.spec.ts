import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReferenceAgentComponent } from './reference-agent.component';

describe('ReferenceAgentComponent', () => {
  let component: ReferenceAgentComponent;
  let fixture: ComponentFixture<ReferenceAgentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReferenceAgentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReferenceAgentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
