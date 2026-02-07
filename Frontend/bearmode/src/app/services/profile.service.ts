import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, throwError, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import type { Profile, ProfileCreate, ProfileUpdate } from '../models/profile';

@Injectable({ providedIn: 'root' })
export class ProfileService {
  private readonly baseUrl = `${environment.apiUrl}/profiles`;

  readonly selectedProfile = signal<Profile | null>(null);

  constructor(private readonly http: HttpClient) {
    this.loadSelectedProfile();
  }

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
    return this.http.delete<void>(`${this.baseUrl}/${id}`).pipe(
      tap(() => {
        const current = this.selectedProfile();
        if (current && current.id === id) {
          this.selectedProfile.set(null);
          localStorage.removeItem('selectedProfile');
        }
      }),
      catchError(this.handleError)
    );
  }

  selectProfile(profile: Profile): void {
    this.selectedProfile.set(profile);
    localStorage.setItem('selectedProfile', JSON.stringify(profile));
  }

  private loadSelectedProfile(): void {
    const savedProfile = localStorage.getItem('selectedProfile');
    if (savedProfile) {
      try {
        this.selectedProfile.set(JSON.parse(savedProfile));
      } catch (e) {
        console.error('Failed to parse selected profile from local storage', e);
        localStorage.removeItem('selectedProfile');
      }
    }
  }

  private handleError(error: { status?: number; error?: { detail?: string }; message?: string }) {
    const detail =
      typeof error?.error?.detail === 'string'
        ? error.error.detail
        : error?.message ?? 'Unbekannter Fehler';
    return throwError(() => ({ status: error?.status, detail }));
  }
}
