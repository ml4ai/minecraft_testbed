import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MapParentComponent } from './map-parent.component';

describe('MapParentComponent', () => {
  let component: MapParentComponent;
  let fixture: ComponentFixture<MapParentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MapParentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MapParentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
