import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { TrainingPlanService } from '../../../services/training-plan.service';
import type { TrainingPlanExecuteResponse } from '../../../models/training-plan';
import { TrainingExecuteTimerComponent } from '../training-execute-timer/training-execute-timer.component';
import { TrainingExecuteTableComponent } from '../training-execute-table/training-execute-table.component';

@Component({
    selector: 'app-training-execute-session',
    standalone: true,
    imports: [
        CommonModule,
        MatButtonModule,
        TrainingExecuteTimerComponent,
        TrainingExecuteTableComponent
    ],
    templateUrl: './training-execute-session.component.html',
})
export class TrainingExecuteSessionComponent implements OnInit {
    plan = signal<TrainingPlanExecuteResponse | null>(null);
    loading = signal(true);
    error = signal<string | null>(null);

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private trainingPlanService: TrainingPlanService
    ) { }

    ngOnInit(): void {
        const planId = this.route.snapshot.paramMap.get('id');
        if (!planId) {
            this.error.set('Keine Plan-ID gefunden.');
            this.loading.set(false);
            return;
        }

        this.loadPlan(planId);
    }

    loadPlan(id: string) {
        this.loading.set(true);
        this.trainingPlanService.getExecutePlan(id).subscribe({
            next: (data) => {
                this.plan.set(data);
                this.loading.set(false);
            },
            error: (err: any) => {
                console.error('Error loading execution plan', err);
                this.error.set('Fehler beim Laden des Plans.');
                this.loading.set(false);
            }
        });
    }

    goBack() {
        this.router.navigate(['/training-execute']);
    }
}
