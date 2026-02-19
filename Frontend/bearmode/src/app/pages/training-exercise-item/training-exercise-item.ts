import { Component, OnInit, signal, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
import { TrainingExerciseItemService } from '../../services/training-exercise-item.service';
import { BodyCategoryService } from '../../services/body-category.service';
import type { TrainingExerciseItem } from '../../models/training-exercise-item';
import type { BodyCategory } from '../../models/body-category';

@Component({
  selector: 'app-training-exercise-item',
  standalone: true,
  imports: [
    FormsModule,
    MatTableModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatSnackBarModule,
    MatDialogModule
  ],
  templateUrl: './training-exercise-item.html',
  styleUrl: './training-exercise-item.css'
})
export class TrainingExerciseItemComponent implements OnInit {
  readonly dataSource = new MatTableDataSource<TrainingExerciseItem>([]);
  readonly displayedColumns: string[] = ['description', 'body_category', 'video_url', 'actions'];
  readonly loading = signal(false);
  readonly errorMessage = signal<string | null>(null);

  readonly bodyCategories = signal<BodyCategory[]>([]);

  /** Create/Edit form state: null = closed, { id?: string, ...values } = open */
  readonly formState = signal<{ id?: string; description: string; video_url: string; body_category_id: string } | null>(null);
  /** Bound to inputs (ngModel) */
  formDescriptionValue = '';
  formVideoUrlValue = '';
  formBodyCategoryIdValue = '';
  readonly formSaving = signal(false);

  readonly isEditMode = computed(() => {
    const s = this.formState();
    return s != null && 'id' in s && s.id != null;
  });

  constructor(
    private readonly service: TrainingExerciseItemService,
    private readonly bodyCategoryService: BodyCategoryService,
    private readonly snackBar: MatSnackBar,
    private readonly dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.loadBodyCategories();
    this.loadItems();
  }

  loadBodyCategories(): void {
    this.bodyCategoryService.getAll().subscribe({
      next: (categories) => this.bodyCategories.set(categories),
      error: () => this.snackBar.open('Fehler beim Laden der Körperkategorien', 'OK', { duration: 3000 })
    });
  }

  loadItems(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.service.getAll().subscribe({
      next: (items) => {
        this.dataSource.data = items;
        this.loading.set(false);
      },
      error: (err) => {
        this.loading.set(false);
        this.errorMessage.set(err?.detail ?? 'Fehler beim Laden der Übungen.');
      }
    });
  }

  openCreate(): void {
    // Default to first category if available, or empty
    const firstCat = this.bodyCategories()[0]?.id || '';
    this.formState.set({ description: '', video_url: '', body_category_id: firstCat });
    this.formDescriptionValue = '';
    this.formVideoUrlValue = '';
    this.formBodyCategoryIdValue = firstCat;
  }

  openEdit(item: TrainingExerciseItem): void {
    this.formState.set({
      id: item.id,
      description: item.description,
      video_url: item.video_url || '',
      body_category_id: item.body_category.id
    });
    this.formDescriptionValue = item.description;
    this.formVideoUrlValue = item.video_url || '';
    this.formBodyCategoryIdValue = item.body_category.id;
  }

  cancelForm(): void {
    this.formState.set(null);
    this.formDescriptionValue = '';
    this.formVideoUrlValue = '';
    this.formBodyCategoryIdValue = '';
  }

  saveForm(): void {
    const description = this.formDescriptionValue.trim();
    let video_url = this.formVideoUrlValue.trim() || null;
    const body_category_id = this.formBodyCategoryIdValue;

    if (!description) {
      this.snackBar.open('Bitte eine Beschreibung eingeben.', 'OK', { duration: 3000 });
      return;
    }

    if (!body_category_id) {
      this.snackBar.open('Bitte eine Körperkategorie wählen.', 'OK', { duration: 3000 });
      return;
    }

    if (video_url) {
      try {
        new URL(video_url);
      } catch (_) {
        this.snackBar.open('Bitte eine gültige Video-URL eingeben.', 'OK', { duration: 3000 });
        return;
      }
    }

    const state = this.formState();
    if (!state) return;

    this.formSaving.set(true);
    const sub = state.id
      ? this.service.update(state.id, { description, video_url, body_category_id })
      : this.service.create({ description, video_url, body_category_id });

    sub.subscribe({
      next: () => {
        this.formSaving.set(false);
        this.cancelForm();
        this.loadItems();
        this.snackBar.open(state.id ? 'Übung aktualisiert.' : 'Übung erstellt.', 'OK', {
          duration: 3000
        });
      },
      error: (err) => {
        this.formSaving.set(false);
        const msg =
          err?.status === 409
            ? 'Eine Übung mit dieser Beschreibung existiert bereits.'
            : err?.detail ?? 'Aktion fehlgeschlagen.';
        this.snackBar.open(msg, 'OK', { duration: 5000 });
      }
    });
  }

  deleteItem(item: TrainingExerciseItem): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Übung löschen',
        message: `Möchten Sie die Übung „${item.description}“ wirklich löschen?`,
        confirmText: 'Löschen',
        confirmColor: 'warn'
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.service.delete(item.id).subscribe({
          next: () => {
            this.loadItems();
            this.snackBar.open('Übung gelöscht.', 'OK', { duration: 3000 });
          },
          error: (err) => {
            const msg =
              err?.status === 404
                ? 'Übung wurde nicht gefunden.'
                : err?.detail ?? 'Löschen fehlgeschlagen.';
            this.snackBar.open(msg, 'OK', { duration: 5000 });
          }
        });
      }
    });
  }
}
