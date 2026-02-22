import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class DataSyncService {
    private http = inject(HttpClient);
    private apiUrl = `${environment.apiUrl}/data-sync`;

    exportData(): Observable<any> {
        return this.http.get(`${this.apiUrl}/export`);
    }

    importData(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/import`, data);
    }
}
