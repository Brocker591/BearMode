import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { TrainingPlanService } from '../../../services/training-plan.service';
import { ProfileService } from '../../../services/profile.service';
import type { TrainingPlan } from '../../../models/training-plan';
import type { Profile } from '../../../models/profile';

@Component({
    selector: 'app-training-execute-list',
    standalone: true,
    imports: [
        CommonModule,
        MatTableModule,
        MatButtonModule,
        MatIconModule
    ],
    templateUrl: './training-execute-list.component.html',
    styles: [`
        .example-element-row {
            cursor: pointer;
        }
        .example-element-row:hover {
            background: #f5f5f5;
        }
        .example-element-row:active {
            background: #efefef;
        }
        .example-element-detail {
            overflow: hidden;
            display: flex;
        }
        tr.example-detail-row {
            height: 0;
        }
        .inner-table {
            width: 100%;
            border-collapse: collapse;
        }
        .inner-table th, .inner-table td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .inner-table th {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #f2f2f2;
            color: black;
        }
    `],
    animations: [
        trigger('detailExpand', [
            state('collapsed,void', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
        ]),
    ],
})
export class TrainingExecuteListComponent implements OnInit {
    readonly dataSource = new MatTableDataSource<TrainingPlan>([]);
    readonly displayedColumns: string[] = ['name', 'profile', 'actions'];
    readonly loading = signal(false);
    readonly errorMessage = signal<string | null>(null);
    expandedElement: TrainingPlan | null = null;
    readonly profiles = signal<Profile[]>([]);

    constructor(
        private readonly trainingPlanService: TrainingPlanService,
        private readonly profileService: ProfileService,
        private readonly router: Router
    ) { }

    ngOnInit(): void {
        this.loadProfiles();
        this.loadPlans();
    }

    loadProfiles(): void {
        this.profileService.getAll().subscribe({
            next: (p) => this.profiles.set(p),
            error: (err: any) => console.error('Failed to load profiles', err)
        });
    }

    loadPlans(): void {
        this.loading.set(true);
        this.errorMessage.set(null);
        this.trainingPlanService.getAll().subscribe({
            next: (plans) => {
                this.dataSource.data = plans;
                this.loading.set(false);
            },
            error: (err: any) => {
                this.loading.set(false);
                this.errorMessage.set(err?.detail ?? 'Fehler beim Laden der Trainingspläne.');
            }
        });
    }

    getProfileName(profileId: string): string {
        const p = this.profiles().find(x => x.id === profileId);
        return p ? p.name : 'Unbekannt';
    }

    executePlan(plan: TrainingPlan, event: Event): void {
        event.stopPropagation();
        this.router.navigate(['/training-execute', plan.id]);
    }
}
