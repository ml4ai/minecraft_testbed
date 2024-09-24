import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InteractionPaneComponent } from './interaction-pane.component';

describe('InteractionPaneComponent', () => {
  let component: InteractionPaneComponent;
  let fixture: ComponentFixture<InteractionPaneComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InteractionPaneComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InteractionPaneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
