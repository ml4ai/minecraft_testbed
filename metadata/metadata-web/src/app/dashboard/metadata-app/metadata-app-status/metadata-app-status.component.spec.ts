import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MetadataAppStatusComponent } from './metadata-app-status.component';

describe('MetadataAppStatusComponent', () => {
  let component: MetadataAppStatusComponent;
  let fixture: ComponentFixture<MetadataAppStatusComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MetadataAppStatusComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MetadataAppStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
