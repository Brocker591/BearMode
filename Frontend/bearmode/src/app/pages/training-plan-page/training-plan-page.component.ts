import { Component, OnInit, signal, computed, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common'; // Import CommonModule
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select'; // Need select for Profile
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon'; // Import MatIconModule
import { trigger, state, style, transition, animate } from '@angular/animations'; // Import animations
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
import { TrainingPlanService } from '../../services/training-plan.service';
import { ProfileService } from '../../services/profile.service'; // Need to load profiles
import type { TrainingPlan } from '../../models/training-plan';
import type { Profile } from '../../models/profile';

import { TrainingPlanWizardComponent } from './training-plan-wizard/training-plan-wizard.component';

@Component({
    selector: 'app-training-plan-page',
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        MatTableModule,
        MatButtonModule,
        MatFormFieldModule,
        MatInputModule,
        MatSelectModule,
        MatSnackBarModule,
        MatDialogModule,
        MatIconModule
    ],
    templateUrl: './training-plan-page.component.html',
    styleUrls: ['./training-plan-page.component.css'],
    animations: [
        trigger('detailExpand', [
            state('collapsed,void', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
        ]),
    ],
})
export class TrainingPlanPageComponent implements OnInit {
    readonly dataSource = new MatTableDataSource<TrainingPlan>([]);
    // Removed 'exerciseCount' from displayedColumns
    readonly displayedColumns: string[] = ['name', 'profile', 'actions'];
    readonly loading = signal(false);
    readonly errorMessage = signal<string | null>(null);
    expandedElement: TrainingPlan | null = null;

    // Profile Data for Dropdown
    readonly profiles = signal<Profile[]>([]);

    readonly selectedProfile: WritableSignal<Profile | null>;

    constructor(
        private readonly trainingPlanService: TrainingPlanService,
        private readonly profileService: ProfileService,
        private readonly snackBar: MatSnackBar,
        private readonly dialog: MatDialog
    ) {
        this.selectedProfile = this.profileService.selectedProfile;
    }

    ngOnInit(): void {
        this.loadProfiles();
        this.loadPlans();
    }

    loadProfiles(): void {
        this.profileService.getAll().subscribe({
            next: (p) => this.profiles.set(p),
            error: (err) => console.error('Failed to load profiles', err)
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
            error: (err) => {
                this.loading.set(false);
                this.errorMessage.set(err?.detail ?? 'Fehler beim Laden der Trainingspläne.');
            }
        });
    }

    getProfileName(profileId: string): string {
        const p = this.profiles().find(x => x.id === profileId);
        return p ? p.name : 'Unbekannt';
    }

    openCreate(): void {
        const dialogRef = this.dialog.open(TrainingPlanWizardComponent, {
            width: '90%',
            maxWidth: '1200px',
            height: '80vh',
            disableClose: true
        });

        dialogRef.afterClosed().subscribe(result => {
            if (result) {
                this.loadPlans();
            }
        });
    }

    openEdit(plan: TrainingPlan, event: Event): void {
        // Prevent row expansion when clicking edit
        event.stopPropagation();
        const dialogRef = this.dialog.open(TrainingPlanWizardComponent, {
            width: '90%',
            maxWidth: '1200px',
            height: '80vh',
            disableClose: true,
            data: plan // Pass plan data for editing
        });

        dialogRef.afterClosed().subscribe(result => {
            if (result) {
                this.loadPlans();
            }
        });
    }

    deletePlan(plan: TrainingPlan, event: Event): void {
        // Prevent row expansion when clicking delete
        event.stopPropagation();
        const dialogRef = this.dialog.open(ConfirmDialogComponent, {
            data: {
                title: 'Plan löschen',
                message: `Möchten Sie den Plan „${plan.name}“ wirklich löschen?`,
                confirmText: 'Löschen',
                confirmColor: 'warn'
            }
        });

        dialogRef.afterClosed().subscribe((result) => {
            if (result) {
                this.trainingPlanService.delete(plan.id).subscribe({
                    next: () => {
                        this.loadPlans();
                        this.snackBar.open('Plan gelöscht.', 'OK', { duration: 3000 });
                    },
                    error: (err) => {
                        this.snackBar.open(err?.detail ?? 'Löschen fehlgeschlagen.', 'OK', { duration: 5000 });
                    }
                });
            }
        });
    }
}

