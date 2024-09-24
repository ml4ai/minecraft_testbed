import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExportTimeWindowComponent } from './export-time-window.component';

describe('ExportTimeWindowComponent', () => {
  let component: ExportTimeWindowComponent;
  let fixture: ComponentFixture<ExportTimeWindowComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExportTimeWindowComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExportTimeWindowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
