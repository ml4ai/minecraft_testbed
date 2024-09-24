import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ObserverInfoComponent } from './observer-info.component';

describe('ObserverInfoComponent', () => {
  let component: ObserverInfoComponent;
  let fixture: ComponentFixture<ObserverInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ObserverInfoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ObserverInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
