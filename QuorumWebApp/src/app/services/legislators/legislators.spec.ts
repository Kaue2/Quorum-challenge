import { TestBed } from '@angular/core/testing';

import { Legislators } from './legislators';

describe('Legislators', () => {
  let service: Legislators;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Legislators);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
