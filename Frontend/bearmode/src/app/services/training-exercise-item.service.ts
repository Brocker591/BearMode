import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import type {
    TrainingExerciseItem,
    TrainingExerciseItemCreate,
    TrainingExerciseItemUpdate
} from '../models/training-exercise-item';

@Injectable({ providedIn: 'root' })
export class TrainingExerciseItemService {
    private readonly baseUrl = `${environment.apiUrl}/training-exercise-items`;

    constructor(private readonly http: HttpClient) { }

    getAll(): Observable<TrainingExerciseItem[]> {
        return this.http.get<TrainingExerciseItem[]>(this.baseUrl).pipe(catchError(this.handleError));
    }

    getById(id: string): Observable<TrainingExerciseItem> {
        return this.http.get<TrainingExerciseItem>(`${this.baseUrl}/${id}`).pipe(catchError(this.handleError));
    }

    create(body: TrainingExerciseItemCreate): Observable<TrainingExerciseItem> {
        return this.http.post<TrainingExerciseItem>(this.baseUrl, body).pipe(catchError(this.handleError));
    }

    update(id: string, body: TrainingExerciseItemUpdate): Observable<TrainingExerciseItem> {
        return this.http.put<TrainingExerciseItem>(`${this.baseUrl}/${id}`, body).pipe(catchError(this.handleError));
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
