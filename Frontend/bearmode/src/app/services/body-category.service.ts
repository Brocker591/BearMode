import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import type {
    BodyCategory,
    BodyCategoryCreate,
    BodyCategoryUpdate
} from '../models/body-category';

@Injectable({ providedIn: 'root' })
export class BodyCategoryService {
    private readonly baseUrl = `${environment.apiUrl}/body-categories`;

    constructor(private readonly http: HttpClient) { }

    getAll(): Observable<BodyCategory[]> {
        return this.http.get<BodyCategory[]>(this.baseUrl).pipe(catchError(this.handleError));
    }

    getById(id: string): Observable<BodyCategory> {
        return this.http.get<BodyCategory>(`${this.baseUrl}/${id}`).pipe(catchError(this.handleError));
    }

    create(body: BodyCategoryCreate): Observable<BodyCategory> {
        return this.http.post<BodyCategory>(this.baseUrl, body).pipe(catchError(this.handleError));
    }

    update(id: string, body: BodyCategoryUpdate): Observable<BodyCategory> {
        return this.http.put<BodyCategory>(this.baseUrl, { id, ...body }).pipe(catchError(this.handleError));
    }

    delete(id: string): Observable<void> {
        return this.http.delete<void>(`${this.baseUrl}/${id}`).pipe(catchError(this.handleError));
    }

    private handleError(error: { status?: number; error?: { detail?: string }; message?: string }) {
        const detail =
            typeof error?.error?.detail === 'string'
                ? error.error.detail
                : error?.message ?? 'Unbekannter Fehler';
        return throwError(() => ({ status: error?.status, detail }));
    }
}
