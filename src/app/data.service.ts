import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Device } from './Device-class';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private dailyJsonUrl ='http://10.186.125.101:5000/daily';
  private historicJsonUrl ='http://192.168.0.100:5000/historic';

  constructor(private http: HttpClient) { }

  getData(historic: Boolean): Observable<Device[]> {
    let finalUrl= this.dailyJsonUrl;
    if (historic==true){
      finalUrl= this.historicJsonUrl;
    }
    return this.http.get<Device[]>(finalUrl);
  }

}
