import { Component, OnInit, signal, computed } from '@angular/core';
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
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
import { TrainingPlanService } from '../../services/training-plan.service';
import { ProfileService } from '../../services/profile.service'; // Need to load profiles
import type { TrainingPlan } from '../../models/training-plan';
import type { Profile } from '../../models/profile';

@Component({
    selector: 'app-training-plan-page',
    standalone: true,
    imports: [
        CommonModule, // Add CommonModule here
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
    styleUrls: ['./training-plan-page.component.css']
})
export class TrainingPlanPageComponent implements OnInit {
    readonly dataSource = new MatTableDataSource<TrainingPlan>([]);
    readonly displayedColumns: string[] = ['name', 'profile', 'exerciseCount', 'actions'];
    readonly loading = signal(false);
    readonly errorMessage = signal<string | null>(null);

    // Profile Data for Dropdown
    readonly profiles = signal<Profile[]>([]);

    // Form State
    readonly formState = signal<{ id?: string; name: string; profile_id: string } | null>(null);
    formNameValue = '';
    formProfileIdValue = '';
    readonly formSaving = signal(false);

    readonly isEditMode = computed(() => {
        const s = this.formState();
        return s != null && 'id' in s && s.id != null;
    });

    constructor(
        private readonly trainingPlanService: TrainingPlanService,
        private readonly profileService: ProfileService,
        private readonly snackBar: MatSnackBar,
        private readonly dialog: MatDialog
    ) { }

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
        this.formState.set({ name: '', profile_id: '' });
        this.formNameValue = '';
        this.formProfileIdValue = '';
    }

    openEdit(plan: TrainingPlan): void {
        this.formState.set({ id: plan.id, name: plan.name, profile_id: plan.profile_id });
        this.formNameValue = plan.name;
        this.formProfileIdValue = plan.profile_id;
    }

    cancelForm(): void {
        this.formState.set(null);
        this.formNameValue = '';
        this.formProfileIdValue = '';
    }

    saveForm(): void {
        const name = this.formNameValue.trim();
        const profileId = this.formProfileIdValue;

        if (!name) {
            this.snackBar.open('Bitte einen Namen eingeben.', 'OK', { duration: 3000 });
            return;
        }
        if (!profileId) {
            this.snackBar.open('Bitte ein Profil auswählen.', 'OK', { duration: 3000 });
            return;
        }

        const state = this.formState();
        if (!state) return;

        this.formSaving.set(true);
        const sub = state.id
            ? this.trainingPlanService.update(state.id, { name, profile_id: profileId, training_exercises: [] }) // Keeping exercises empty/unchanged for now as per minimal CRUD req
            : this.trainingPlanService.create({ name, profile_id: profileId, training_exercises: [] });

        sub.subscribe({
            next: () => {
                this.formSaving.set(false);
                this.cancelForm();
                this.loadPlans();
                this.snackBar.open(state.id ? 'Plan aktualisiert.' : 'Plan erstellt.', 'OK', {
                    duration: 3000
                });
            },
            error: (err) => {
                this.formSaving.set(false);
                this.snackBar.open(err?.detail ?? 'Aktion fehlgeschlagen.', 'OK', { duration: 5000 });
            }
        });
    }

    deletePlan(plan: TrainingPlan): void {
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
