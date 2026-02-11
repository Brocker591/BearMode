import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import type { TrainingExerciseExecuteResponse } from '../../../models/training-plan';

@Component({
    selector: 'app-training-execute-table',
    standalone: true,
    imports: [
        CommonModule,
        MatTableModule,
        MatButtonModule,
        MatIconModule,
        MatTooltipModule
    ],
    templateUrl: './training-execute-table.component.html',
})
export class TrainingExecuteTableComponent implements OnChanges {
    @Input() exercises: TrainingExerciseExecuteResponse[] = [];

    dataSource = new MatTableDataSource<TrainingExerciseExecuteResponse>([]);
    displayedColumns: string[] = ['order', 'description', 'sets_info', 'break_time', 'video'];

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['exercises']) {
            this.dataSource.data = this.exercises;
        }
    }

    openVideo(url: string | null | undefined) {
        if (url) {
            window.open(url, '_blank');
        }
    }
}
