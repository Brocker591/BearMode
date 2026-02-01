import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import type { Profile, ProfileCreate, ProfileUpdate } from '../models/profile';

@Injectable({ providedIn: 'root' })
export class ProfileService {
  private readonly baseUrl = `${environment.apiUrl}/profiles`;

  constructor(private readonly http: HttpClient) {}

  getAll(): Observable<Profile[]> {
    return this.http.get<Profile[]>(this.baseUrl).pipe(catchError(this.handleError));
  }

  getById(id: string): Observable<Profile> {
    return this.http.get<Profile>(`${this.baseUrl}/${id}`).pipe(catchError(this.handleError));
  }

  create(body: ProfileCreate): Observable<Profile> {
    return this.http.post<Profile>(this.baseUrl, body).pipe(catchError(this.handleError));
  }

  update(id: string, body: ProfileUpdate): Observable<Profile> {
    return this.http.put<Profile>(`${this.baseUrl}/${id}`, body).pipe(catchError(this.handleError));
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
