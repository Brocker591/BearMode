import { Component, OnInit, signal, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
import { BodyCategoryService } from '../../services/body-category.service';
import type { BodyCategory } from '../../models/body-category';

@Component({
    selector: 'app-body-category',
    standalone: true,
    imports: [
        FormsModule,
        MatTableModule,
        MatButtonModule,
        MatFormFieldModule,
        MatInputModule,
        MatSnackBarModule,
        MatDialogModule
    ],
    templateUrl: './body-category.component.html',
    styleUrl: './body-category.component.css'
})
export class BodyCategoryComponent implements OnInit {
    readonly dataSource = new MatTableDataSource<BodyCategory>([]);
    readonly displayedColumns: string[] = ['name', 'actions'];
    readonly loading = signal(false);
    readonly errorMessage = signal<string | null>(null);

    /** Create/Edit form state: null = closed, { id?: string, ...values } = open */
    readonly formState = signal<{ id?: string; name: string } | null>(null);
    /** Bound to inputs (ngModel) */
    formNameValue = '';
    readonly formSaving = signal(false);

    readonly isEditMode = computed(() => {
        const s = this.formState();
        return s != null && 'id' in s && s.id != null;
    });

    constructor(
        private readonly service: BodyCategoryService,
        private readonly snackBar: MatSnackBar,
        private readonly dialog: MatDialog
    ) { }

    ngOnInit(): void {
        this.loadItems();
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
                this.errorMessage.set(err?.detail ?? 'Fehler beim Laden der Kategorien.');
            }
        });
    }

    openCreate(): void {
        this.formState.set({ name: '' });
        this.formNameValue = '';
    }

    openEdit(item: BodyCategory): void {
        this.formState.set({ id: item.id, name: item.name });
        this.formNameValue = item.name;
    }

    cancelForm(): void {
        this.formState.set(null);
        this.formNameValue = '';
    }

    saveForm(): void {
        const name = this.formNameValue.trim();

        if (!name) {
            this.snackBar.open('Bitte einen Namen eingeben.', 'OK', { duration: 3000 });
            return;
        }

        const state = this.formState();
        if (!state) return;

        this.formSaving.set(true);
        const sub = state.id
            ? this.service.update(state.id, { name })
            : this.service.create({ name });

        sub.subscribe({
            next: () => {
                this.formSaving.set(false);
                this.cancelForm();
                this.loadItems();
                this.snackBar.open(state.id ? 'Kategorie aktualisiert.' : 'Kategorie erstellt.', 'OK', {
                    duration: 3000
                });
            },
            error: (err) => {
                this.formSaving.set(false);
                const msg =
                    err?.status === 409
                        ? 'Eine Kategorie mit diesem Namen existiert bereits.'
                        : err?.detail ?? 'Aktion fehlgeschlagen.';
                this.snackBar.open(msg, 'OK', { duration: 5000 });
            }
        });
    }

    deleteItem(item: BodyCategory): void {
        const dialogRef = this.dialog.open(ConfirmDialogComponent, {
            data: {
                title: 'Kategorie löschen',
                message: `Möchten Sie die Kategorie „${item.name}“ wirklich löschen?`,
                confirmText: 'Löschen',
                confirmColor: 'warn'
            }
        });

        dialogRef.afterClosed().subscribe((result) => {
            if (result) {
                this.service.delete(item.id).subscribe({
                    next: () => {
                        this.loadItems();
                        this.snackBar.open('Kategorie gelöscht.', 'OK', { duration: 3000 });
                    },
                    error: (err) => {
                        const msg =
                            err?.status === 404
                                ? 'Kategorie wurde nicht gefunden.'
                                : err?.detail ?? 'Löschen fehlgeschlagen.';
                        this.snackBar.open(msg, 'OK', { duration: 5000 });
                    }
                });
            }
        });
    }
}
