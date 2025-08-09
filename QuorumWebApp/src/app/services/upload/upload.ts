import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  requestUrl = environment.apiUrl;
  constructor(private httpClient: HttpClient){}

  uploadFiles(formData: FormData){
    return this.httpClient.post(this.requestUrl + "/upload-csvs", formData);
  }
}
