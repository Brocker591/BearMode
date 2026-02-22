import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import type {
    TrainingPlan,
    TrainingPlanCreate,
    TrainingPlanUpdate,
    TrainingPlanExecuteResponse,
    TrainingExerciseCompletion,
    TrainingPlanCompletion
} from '../models/training-plan';

@Injectable({ providedIn: 'root' })
export class TrainingPlanService {
    private readonly baseUrl = `${environment.apiUrl}/training-plans`;

    constructor(private readonly http: HttpClient) { }

    getAll(): Observable<TrainingPlan[]> {
        return this.http.get<TrainingPlan[]>(this.baseUrl).pipe(catchError(this.handleError));
    }

    getAllByProfileId(profileId: string): Observable<TrainingPlan[]> {
        return this.http.get<TrainingPlan[]>(`${this.baseUrl}/byProfileId/${profileId}`).pipe(catchError(this.handleError));
    }

    getById(id: string): Observable<TrainingPlan> {
        return this.http.get<TrainingPlan>(`${this.baseUrl}/${id}`).pipe(catchError(this.handleError));
    }

    create(body: TrainingPlanCreate): Observable<TrainingPlan> {
        return this.http.post<TrainingPlan>(this.baseUrl, body).pipe(catchError(this.handleError));
    }

    update(body: TrainingPlanUpdate): Observable<TrainingPlan> {
        return this.http.put<TrainingPlan>(this.baseUrl, body).pipe(catchError(this.handleError));
    }

    delete(id: string): Observable<void> {
        return this.http.delete<void>(`${this.baseUrl}/${id}`).pipe(catchError(this.handleError));
    }

    getExecutePlan(id: string): Observable<TrainingPlanExecuteResponse> {
        return this.http.get<TrainingPlanExecuteResponse>(`${this.baseUrl}/${id}/execute`)
            .pipe(catchError(this.handleError));
    }

    complete(exercises: TrainingExerciseCompletion[]): Observable<void> {
        return this.http.post<void>(`${environment.apiUrl}/exercice-completion`, exercises)
            .pipe(catchError(this.handleError));
    }

    completePlan(planCompletions: TrainingPlanCompletion[]): Observable<void> {
        return this.http.post<void>(`${environment.apiUrl}/training-plan-completion`, planCompletions)
            .pipe(catchError(this.handleError));
    }

    private handleError(error: { status?: number; error?: { detail?: string }; message?: string }) {
        const detail =
            typeof error?.error?.detail === 'string'
                ? error.error.detail
                : error?.message ?? 'Unbekannter Fehler';
        return throwError(() => ({ status: error?.status, detail }));
    }

    getCompletionHistory(profileId: string): Observable<TrainingExerciseCompletion[]> {
        return this.http.get<TrainingExerciseCompletion[]>(`${environment.apiUrl}/exercice-completion/byProfileId/${profileId}`)
            .pipe(catchError(this.handleError));
    }

    getPlanCompletionHistory(profileId: string): Observable<TrainingPlanCompletion[]> {
        return this.http.get<TrainingPlanCompletion[]>(`${environment.apiUrl}/training-plan-completion/byProfileId/${profileId}`)
            .pipe(catchError(this.handleError));
    }
}
