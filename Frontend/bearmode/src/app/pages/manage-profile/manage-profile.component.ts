import { Component, OnInit, signal, computed } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
import { ProfileService } from '../../services/profile.service';
import type { Profile } from '../../models/profile';

import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-manage-profile',
  standalone: true,
  imports: [
    FormsModule,
    MatTableModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSnackBarModule,
    MatDialogModule,
    MatIconModule
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

  // Animal emojis for profiles (same as SelectProfile)
  readonly animalEmojis = ['🐻', '🦁', '🐯', '🐨', '🐼', '🦊', '🐰', '🐹', '🐶', '🐱', '🐸', '🐙', '🦄', '🐲', '🦉', '🦜', '🦝', '🐗'];

  constructor(
    private readonly profileService: ProfileService,
    private readonly snackBar: MatSnackBar,
    private readonly dialog: MatDialog,
    private readonly route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.loadProfiles();
    this.route.queryParams.subscribe(params => {
      if (params['create'] === 'true') {
        this.openCreate();
      }
    });
  }

  getProfileEmoji(profile: Profile): string {
    let hash = 0;
    if (profile.id) {
      for (let i = 0; i < profile.id.length; i++) {
        hash = profile.id.charCodeAt(i) + ((hash << 5) - hash);
      }
    } else {
      // Fallback if no ID (shouldnt happen on saved profiles)
      for (let i = 0; i < profile.name.length; i++) {
        hash = profile.name.charCodeAt(i) + ((hash << 5) - hash);
      }
    }
    const index = Math.abs(hash % this.animalEmojis.length);
    return this.animalEmojis[index];
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
      next: (profile) => {
        this.formSaving.set(false);
        this.cancelForm();
        this.loadProfiles();

        // Auto-select if no profile is currently selected
        if (!this.profileService.selectedProfile()) {
          this.profileService.selectProfile(profile);
        }

        this.snackBar.open(state.id ? 'Profil aktualisiert.' : 'Profil verwendet und erstellt.', 'OK', {
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
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Profil löschen',
        message: `Möchten Sie das Profil „${profile.name}“ wirklich löschen?`,
        confirmText: 'Löschen',
        confirmColor: 'warn'
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
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
    });
  }
}
