import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatCheckboxModule } from '@angular/material/checkbox';
import type { TrainingExerciseExecuteResponse, TrainingExerciseCompletion } from '../../../models/training-plan';
import { TrainingPlanService } from '../../../services/training-plan.service';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
    selector: 'app-training-execute-table',
    standalone: true,
    imports: [
        CommonModule,
        MatTableModule,
        MatButtonModule,
        MatIconModule,
        MatTooltipModule,
        MatTooltipModule,
        MatCheckboxModule,
        MatSnackBarModule
    ],
    templateUrl: './training-execute-table.component.html',
    styles: [`
        .completed-row {
            background-color: #f9fafb;
        }
        .completed-row td {
            color: #9ca3af !important;
        }
        .completed-text {
            text-decoration: line-through;
            color: #9ca3af;
        }
    `]
})
export class TrainingExecuteTableComponent implements OnChanges {
    @Input() exercises: TrainingExerciseExecuteResponse[] = [];
    @Input() profileId!: string;
    @Input() trainingPlanId!: string;

    constructor(
        private trainingPlanService: TrainingPlanService,
        private snackBar: MatSnackBar,
        private router: Router
    ) { }

    dataSource = new MatTableDataSource<TrainingExerciseExecuteResponse>([]);
    displayedColumns: string[] = ['completed', 'order', 'description', 'sets_info', 'break_time', 'video'];

    completedExercises = new Set<string>(); // Stores IDs of completed exercises

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['exercises']) {
            this.dataSource.data = this.exercises;
        }
    }

    toggleCompletion(exercise: TrainingExerciseExecuteResponse) {
        if (this.completedExercises.has(exercise.id)) {
            this.completedExercises.delete(exercise.id);
        } else {
            this.completedExercises.add(exercise.id);
        }
    }

    isCompleted(exercise: TrainingExerciseExecuteResponse): boolean {
        return this.completedExercises.has(exercise.id);
    }

    completeTraining() {
        if (this.completedExercises.size === 0) {
            this.snackBar.open('Bitte schließen Sie mindestens eine Übung ab.', 'Ok', { duration: 3000 });
            return;
        }

        const completions: TrainingExerciseCompletion[] = [];

        this.exercises.forEach(exercise => {
            if (this.completedExercises.has(exercise.id)) {
                completions.push({
                    id: crypto.randomUUID(),
                    profile_id: this.profileId,
                    training_plan_id: this.trainingPlanId,
                    exercise_id: exercise.exercise_id,
                    order: exercise.order,
                    equipment: exercise.equipment,
                    reps: exercise.reps,
                    break_time_seconds: exercise.break_time_seconds,
                    training_exercise_description: exercise.training_exercise_description,
                    training_exercise_video_url: exercise.training_exercise_video_url
                });
            }
        });

        this.trainingPlanService.complete(completions).subscribe({
            next: () => {
                this.snackBar.open('Training erfolgreich abgeschlossen!', 'Ok', { duration: 3000 });
                this.router.navigate(['/training-plans']);
            },
            error: (err) => {
                console.error('Fehler beim Abschließen des Trainings', err);
                this.snackBar.open('Fehler beim Speichern des Trainings.', 'Ok', { duration: 3000 });
            }
        });
    }




    openVideo(url: string | null | undefined) {
        if (url) {
            window.open(url, '_blank');
        }
    }
}
