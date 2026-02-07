
import { Component, OnInit, signal } from '@angular/core';
import { Router } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ProfileService } from '../../services/profile.service';
import type { Profile } from '../../models/profile';

@Component({
    selector: 'app-select-profile',
    standalone: true,
    imports: [MatButtonModule, MatCardModule, MatProgressSpinnerModule],
    template: `
    <div class="container">
      <h1>Profil auswählen</h1>
      
      @if (loading()) {
        <mat-spinner></mat-spinner>
      } @else {
        <div class="profile-list">
          @for (profile of profiles(); track profile.id) {
            <mat-card class="profile-card" (click)="selectProfile(profile)">
              <mat-card-content>
                {{ profile.name }}
              </mat-card-content>
            </mat-card>
          }
        </div>
        
        <div class="actions">
          <button mat-stroked-button (click)="createProfile()">Neues Profil erstellen</button>
        </div>
      }
    </div>
  `,
    styles: [`
    .container {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem;
      gap: 2rem;
    }
    .profile-list {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      justify-content: center;
    }
    .profile-card {
      width: 200px;
      height: 100px;
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .profile-card:hover {
      transform: scale(1.05);
      background-color: #f0f0f0;
    }
    .actions {
      margin-top: 2rem;
    }
  `]
})
export class SelectProfileComponent implements OnInit {
    readonly profiles = signal<Profile[]>([]);
    readonly loading = signal(false);

    constructor(
        private readonly profileService: ProfileService,
        private readonly router: Router
    ) { }

    ngOnInit(): void {
        this.createProfileIfNone();
    }

    createProfileIfNone(): void {
        this.loading.set(true);
        this.profileService.getAll().subscribe({
            next: (profiles) => {
                this.profiles.set(profiles);
                this.loading.set(false);
                if (profiles.length === 0) {
                    this.createProfile();
                }
            },
            error: () => {
                this.loading.set(false);
                // Handle error?
            }
        });
    }

    selectProfile(profile: Profile): void {
        this.profileService.selectProfile(profile);
        this.router.navigate(['/']);
    }

    createProfile(): void {
        this.router.navigate(['/manage-profile'], { queryParams: { create: 'true' } });
    }
}
