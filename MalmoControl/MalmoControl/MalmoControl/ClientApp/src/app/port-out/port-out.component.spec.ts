import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PortOutComponent } from './port-out.component';

describe('PortOutComponent', () => {
  let component: PortOutComponent;
  let fixture: ComponentFixture<PortOutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PortOutComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PortOutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
