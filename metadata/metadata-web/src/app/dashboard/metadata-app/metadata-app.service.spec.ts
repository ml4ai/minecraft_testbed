import { TestBed } from '@angular/core/testing';

import { MetadataAppService } from './metadata-app.service';

describe('MetadataAppService', () => {
  let service: MetadataAppService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MetadataAppService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
