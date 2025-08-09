import { TestBed } from '@angular/core/testing';

import { Bills } from './bills';

describe('Bills', () => {
  let service: Bills;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Bills);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
