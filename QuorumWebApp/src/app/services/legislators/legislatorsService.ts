import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { LegislatorsSummary } from '../../models/legislators-summary';

@Injectable({
  providedIn: 'root'
})
export class LegislatorsService {
  requestUrl: string = environment.apiUrl + "/legislators"

  constructor(private httpClient: HttpClient){}

  get_legislators_summary(){
    return this.httpClient.get<LegislatorsSummary[]>(this.requestUrl + "/summary");
  }
}
