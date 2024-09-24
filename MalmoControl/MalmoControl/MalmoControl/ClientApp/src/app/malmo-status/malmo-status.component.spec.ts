import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MalmoStatusComponent } from './malmo-status.component';

describe('MalmoStatusComponent', () => {
  let component: MalmoStatusComponent;
  let fixture: ComponentFixture<MalmoStatusComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MalmoStatusComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MalmoStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
