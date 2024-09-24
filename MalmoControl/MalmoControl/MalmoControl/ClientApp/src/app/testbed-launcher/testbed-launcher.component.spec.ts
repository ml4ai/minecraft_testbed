import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TestbedLauncherComponent } from './testbed-launcher.component';

describe('TestbedLauncherComponent', () => {
  let component: TestbedLauncherComponent;
  let fixture: ComponentFixture<TestbedLauncherComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestbedLauncherComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestbedLauncherComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
