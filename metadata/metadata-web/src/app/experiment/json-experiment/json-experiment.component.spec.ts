import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JsonExperimentComponent } from './json-experiment.component';

describe('JsonExperimentComponent', () => {
  let component: JsonExperimentComponent;
  let fixture: ComponentFixture<JsonExperimentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JsonExperimentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JsonExperimentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
