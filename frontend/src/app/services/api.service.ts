import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  connectMySQL(details: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/connect/mysql`, details);
  }

  connectMSSQL(details: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/connect/mssql`, details);
  }

  connectPostgreSQL(details: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/connect/postgresql`, details);
  }

  connectSQLite(details: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/connect/sqlite`, details);
  }
}
