import {
  inject,
  TestBed
} from '@angular/core/testing';
import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { ElasticsearchService } from './elasticsearch.service';

describe('Elasticsearch', () => {
  beforeEach(() => TestBed.configureTestingModule({
    providers: [
      ElasticsearchService
    ]}));

  // it('should return an Observable when test_search called',
  //   inject([ ElasticsearchService], (elasticsearch: ElasticsearchService) => {
  //     expect(elasticsearch.test_search()).toEqual(jasmine.any(Observable));
  //   }));

});
