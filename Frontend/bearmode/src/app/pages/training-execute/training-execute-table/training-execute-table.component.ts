import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatCheckboxModule } from '@angular/material/checkbox';
import type { TrainingExerciseExecuteResponse } from '../../../models/training-plan';

@Component({
    selector: 'app-training-execute-table',
    standalone: true,
    imports: [
        CommonModule,
        MatTableModule,
        MatButtonModule,
        MatIconModule,
        MatTooltipModule,
        MatCheckboxModule
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



    openVideo(url: string | null | undefined) {
        if (url) {
            window.open(url, '_blank');
        }
    }
}
