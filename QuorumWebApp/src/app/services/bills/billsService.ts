import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { BillsSummary } from '../../models/bills-summary';

@Injectable({
  providedIn: 'root'
})
export class BillsService {
  requestUrl: string = environment.apiUrl + "/bills"

  constructor(private httpClient: HttpClient){}

  get_bills_summary(){
    return this.httpClient.get<BillsSummary[]>(this.requestUrl + "/summary");
  }
}
