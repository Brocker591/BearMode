
import { Component, OnInit, signal, computed, WritableSignal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatStepperModule } from '@angular/material/stepper';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatTableModule } from '@angular/material/table';
import { MatSnackBar } from '@angular/material/snack-bar';

import { TrainingPlanService } from '../../../services/training-plan.service';
import { ProfileService } from '../../../services/profile.service';
import { TrainingExerciseItemService } from '../../../services/training-exercise-item.service';

import type { Profile } from '../../../models/profile';
import type { TrainingExerciseItem } from '../../../models/training-exercise-item';
import type { TrainingPlanCreate, TrainingExercise, TrainingPlan, TrainingExerciseCreate, TrainingPlanUpdate } from '../../../models/training-plan';

@Component({
    selector: 'app-training-plan-wizard',
    standalone: true,
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        MatStepperModule,
        MatButtonModule,
        MatFormFieldModule,
        MatInputModule,
        MatSelectModule,
        MatIconModule,
        MatDialogModule,
        MatTableModule
    ],
    templateUrl: './training-plan-wizard.component.html',
    styleUrls: ['./training-plan-wizard.component.css']
})
export class TrainingPlanWizardComponent implements OnInit {
    private readonly fb = inject(FormBuilder);
    private readonly dialogRef = inject(MatDialogRef<TrainingPlanWizardComponent>);
    private readonly data = inject<TrainingPlan | null>(MAT_DIALOG_DATA, { optional: true });
    private readonly trainingPlanService = inject(TrainingPlanService);
    private readonly profileService = inject(ProfileService);
    private readonly trainingExerciseItemService = inject(TrainingExerciseItemService);
    private readonly snackBar = inject(MatSnackBar);

    // Form Groups for Steps
    planDetailsForm: FormGroup;
    exercisesForm: FormGroup; // Contains FormArray

    // Data Signals
    profiles = signal<Profile[]>([]);
    exerciseItems = signal<TrainingExerciseItem[]>([]);
    selectedProfile = this.profileService.selectedProfile;
    isSaving = signal(false);

    // Computed for Overview
    // Data Signals for Overview
    overviewExercises = signal<any[]>([]);

    constructor() {
        this.planDetailsForm = this.fb.group({
            name: ['', Validators.required],
            profile_id: ['', Validators.required]
        });

        this.exercisesForm = this.fb.group({
            exercises: this.fb.array([])
        });

        // Update overview when exercises change
        this.exercisesForm.valueChanges.subscribe(val => {
            this.overviewExercises.set(val.exercises || []);
        });
    }

    ngOnInit(): void {
        // Load Profiles
        this.profileService.getAll().subscribe({
            next: (p) => this.profiles.set(p),
            error: (err) => console.error('Failed to load profiles', err)
        });

        // Load Exercise Items
        this.trainingExerciseItemService.getAll().subscribe({
            next: (items) => this.exerciseItems.set(items),
            error: (err) => console.error('Failed to load exercise items', err)
        });

        // Pre-fill Profile if globally selected
        const globalProfile = this.selectedProfile();
        if (globalProfile) {
            this.planDetailsForm.patchValue({ profile_id: globalProfile.id });
            this.planDetailsForm.get('profile_id')?.disable(); // Lock it if global is set? Or just pre-select? 
            // User requirement: "beim speichern oder beim updaten soll das global verwendete Profil verwendet werden"
            // If we lock it, we ensure this.
        }

        // Check if we are in Edit Mode
        if (this.data) {
            this.populateForm(this.data);
        }
    }

    get isEditMode(): boolean {
        return !!this.data;
    }

    populateForm(plan: TrainingPlan): void {
        this.planDetailsForm.patchValue({
            name: plan.name,
            profile_id: plan.profile_id
        });

        const exercises = plan.exercises || [];
        exercises.sort((a, b) => a.order - b.order).forEach(ex => {
            this.addExercise(ex);
        });
    }

    get exercisesArray(): FormArray {
        return this.exercisesForm.get('exercises') as FormArray;
    }

    addExercise(data?: TrainingExercise): void {
        const exerciseGroup = this.fb.group({
            training_exercise_item_id: [data?.training_exercise_item?.id || '', Validators.required],
            sets: [data?.sets || null],
            reps: [data?.reps || null],
            equipment: [data?.equipment || ''],
            break_time_seconds: [data?.break_time_seconds || 0],
            order: [data ? data.order : this.exercisesArray.length + 1]
        });
        this.exercisesArray.push(exerciseGroup);
    }

    removeExercise(index: number): void {
        this.exercisesArray.removeAt(index);
        // Re-order remaining
        this.exercisesArray.controls.forEach((ctrl, i) => {
            ctrl.patchValue({ order: i + 1 });
        });
    }

    getTrainingExerciseItemName(id: string): string {
        const item = this.exerciseItems().find(x => x.id === id);
        return item ? item.description : 'Unbekannt';
    }

    submitPlan(): void {
        if (this.planDetailsForm.invalid) return;

        this.isSaving.set(true);
        const details = this.planDetailsForm.getRawValue(); // getRawValue to include disabled fields
        const exercises = this.exercisesForm.value.exercises;

        // Map form exercises to model
        const exercisesPayload: TrainingExerciseCreate[] = exercises.map((ex: any, index: number) => ({
            order: index + 1,
            equipment: ex.equipment,
            sets: ex.sets ? Number(ex.sets) : null,
            reps: ex.reps ? Number(ex.reps) : null,
            break_time_seconds: ex.break_time_seconds,
            training_exercise_item_id: ex.training_exercise_item_id
        }));

        const planData: TrainingPlanCreate = {
            name: details.name,
            profile_id: details.profile_id,
            training_exercises: exercisesPayload
        };

        if (this.isEditMode && this.data) {
            // Update
            const updateData: TrainingPlanUpdate = {
                ...planData,
                id: this.data.id
            };
            this.trainingPlanService.update(updateData).subscribe({
                next: () => {
                    this.isSaving.set(false);
                    this.snackBar.open('Trainingsplan erfolgreich aktualisiert!', 'OK', { duration: 3000 });
                    this.dialogRef.close(true);
                },
                error: (err) => {
                    this.isSaving.set(false);
                    this.snackBar.open(err?.detail ?? 'Fehler beim Aktualisieren des Plans.', 'OK', { duration: 5000 });
                }
            });
        } else {
            // Create
            this.trainingPlanService.create(planData).subscribe({
                next: () => {
                    this.isSaving.set(false);
                    this.snackBar.open('Trainingsplan erfolgreich erstellt!', 'OK', { duration: 3000 });
                    this.dialogRef.close(true);
                },
                error: (err) => {
                    this.isSaving.set(false);
                    this.snackBar.open(err?.detail ?? 'Fehler beim Erstellen des Plans.', 'OK', { duration: 5000 });
                }
            });
        }
    }
}
