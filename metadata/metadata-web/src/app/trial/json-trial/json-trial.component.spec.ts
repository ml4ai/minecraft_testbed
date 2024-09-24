import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JsonTrialComponent } from './json-trial.component';

describe('JsonTrialComponent', () => {
  let component: JsonTrialComponent;
  let fixture: ComponentFixture<JsonTrialComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JsonTrialComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JsonTrialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
