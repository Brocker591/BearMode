import { Component, OnInit, signal, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ProfileService } from '../../services/profile.service';
import type { Profile } from '../../models/profile';

@Component({
  selector: 'app-manage-profile',
  standalone: true,
  imports: [
    FormsModule,
    MatTableModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSnackBarModule
  ],
  templateUrl: './manage-profile.component.html',
  styleUrl: './manage-profile.component.css'
})
export class ManageProfileComponent implements OnInit {
  readonly dataSource = new MatTableDataSource<Profile>([]);
  readonly displayedColumns: string[] = ['name', 'actions'];
  readonly loading = signal(false);
  readonly errorMessage = signal<string | null>(null);

  /** Create/Edit form state: null = closed, { id?: string, name: string } = open */
  readonly formState = signal<{ id?: string; name: string } | null>(null);
  /** Bound to the name input (ngModel); set when opening form, read in saveForm(). */
  formNameValue = '';
  readonly formSaving = signal(false);

  readonly isEditMode = computed(() => {
    const s = this.formState();
    return s != null && 'id' in s && s.id != null;
  });

  constructor(
    private readonly profileService: ProfileService,
    private readonly snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadProfiles();
  }

  loadProfiles(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.profileService.getAll().subscribe({
      next: (profiles) => {
        this.dataSource.data = profiles;
        this.loading.set(false);
      },
      error: (err) => {
        this.loading.set(false);
        this.errorMessage.set(err?.detail ?? 'Fehler beim Laden der Profile.');
      }
    });
  }

  openCreate(): void {
    this.formState.set({ name: '' });
    this.formNameValue = '';
  }

  openEdit(profile: Profile): void {
    this.formState.set({ id: profile.id, name: profile.name });
    this.formNameValue = profile.name;
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
      ? this.profileService.update(state.id, { name })
      : this.profileService.create({ name });

    sub.subscribe({
      next: () => {
        this.formSaving.set(false);
        this.cancelForm();
        this.loadProfiles();
        this.snackBar.open(state.id ? 'Profil aktualisiert.' : 'Profil erstellt.', 'OK', {
          duration: 3000
        });
      },
      error: (err) => {
        this.formSaving.set(false);
        const msg =
          err?.status === 409
            ? 'Ein Profil mit diesem Namen existiert bereits.'
            : err?.detail ?? 'Aktion fehlgeschlagen.';
        this.snackBar.open(msg, 'OK', { duration: 5000 });
      }
    });
  }

  deleteProfile(profile: Profile): void {
    if (!confirm(`Profil „${profile.name}“ wirklich löschen?`)) return;
    this.profileService.delete(profile.id).subscribe({
      next: () => {
        this.loadProfiles();
        this.snackBar.open('Profil gelöscht.', 'OK', { duration: 3000 });
      },
      error: (err) => {
        const msg =
          err?.status === 404
            ? 'Profil wurde nicht gefunden.'
            : err?.detail ?? 'Löschen fehlgeschlagen.';
        this.snackBar.open(msg, 'OK', { duration: 5000 });
      }
    });
  }
}
