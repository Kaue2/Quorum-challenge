import { Component } from '@angular/core';
import { LegislatorsSummary } from '../../models/legislators-summary';
import { BillsSummary } from '../../models/bills-summary';
import { LegislatorsService } from '../../services/legislators/legislatorsService';
import { BillsService } from '../../services/bills/billsService';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {
  legislators_summary: LegislatorsSummary[] = [];
  bills_summary: BillsSummary[] = [];
  expectedFiles = ['legislators.csv', 'bills.csv', 'vote_results.csv', 'votes.csv'];
  selectedFiles: { [key: string]: File | null } = {
    'legislators.csv': null,
    'bills.csv': null,
    'vote_results.csv': null,
    'votes.csv': null
  }; 

  constructor(private legislatorsService: LegislatorsService, private billsService: BillsService){}

  ngOnInit(){
    this.legislatorsService.get_legislators_summary().subscribe({
      next: (response) => {
        this.legislators_summary = response;
        //console.log(this.legislators_summary);
      }
    });
    this.billsService.get_bills_summary().subscribe({
      next: (response) => {
        this.bills_summary = response;
        //console.log(this.bills_summary);
      }
    });
  }

  handleFileSelect(event: Event){
    const input = event.target as HTMLInputElement;
    if(!input.files || input.files.length === 0){
      alert("File is null or empty");
      return;
    }

    const file = input.files[0];
    const fileName = file.name.toLowerCase();

    if(this.expectedFiles.includes(fileName)){
      this.selectedFiles[fileName] = file;
      alert(`received file`)
    } else{
      alert(`Invalid file: ${fileName}`)
    }

    input.value = '';
  }

  allFilesSelected(): boolean{
    return Object.values(this.selectedFiles).every(file => file !== null);
  }

  confirmUpload(){
    if(!this.allFilesSelected()){
      alert(`Faild to upload archives`);
      return;
    }

    const formData = new FormData();
    for(const key of Object.keys(this.selectedFiles)){
      formData.append(key.replace('.csv', ''), this.selectedFiles[key]!)
    }
  }
}
