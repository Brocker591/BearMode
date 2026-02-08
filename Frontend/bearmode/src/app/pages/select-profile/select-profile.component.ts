
import { Component, OnInit, signal } from '@angular/core';
import { Router } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ProfileService } from '../../services/profile.service';
import type { Profile } from '../../models/profile';


import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-select-profile',
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatProgressSpinnerModule, MatIconModule],
  template: `
    <div class="page-container">
      <div class="content-wrapper">
        <div class="header">
          <h1>BearMode</h1>
          <p>Wähle dein Profil</p>
        </div>
      
        @if (loading()) {
          <div class="spinner-container">
            <mat-spinner diameter="50"></mat-spinner>
          </div>
        } @else {
          <div class="profile-grid">
            @for (profile of profiles(); track profile.id) {
              <div class="profile-card" (click)="selectProfile(profile)" tabindex="0" (keydown.enter)="selectProfile(profile)">
                <div class="avatar-circle">
                  <span class="emoji-avatar">{{ getProfileEmoji(profile) }}</span>
                </div>
                <span class="profile-name">{{ profile.name }}</span>
              </div>
            }
            
            <!-- Create New Profile Card -->
             <div class="profile-card create-card" (click)="createProfile()" tabindex="0" (keydown.enter)="createProfile()">
                <div class="avatar-circle create-circle">
                  <mat-icon>add</mat-icon>
                </div>
                <span class="profile-name">Neu erstellen</span>
              </div>
          </div>
        }
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      height: 100vh;
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    .page-container {
      min-height: 100vh;
      width: 100%;
      /* Background moved to global styles.css */
      /* background: linear-gradient(135deg, #00F5A0 0%, #00D9F5 100%); */
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 20px;
      box-sizing: border-box;
    }

    .content-wrapper {
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(20px);
      padding: 3rem;
      border-radius: 32px;
      box-shadow: 0 20px 60px rgba(0, 229, 255, 0.25);
      width: 100%;
      max-width: 800px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2rem;
      border: 1px solid rgba(255, 255, 255, 0.6);
    }

    .header {
      text-align: center;
    }

    .header h1 {
      margin: 0;
      font-size: 3.5rem;
      font-weight: 800;
      /* Gradient text */
      background: linear-gradient(45deg, #00bfa5, #0091ea);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -2px;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }

    .header p {
      margin: 0.5rem 0 0;
      font-size: 1.3rem;
      color: #546e7a;
      font-weight: 500;
    }

    .spinner-container {
      display: flex;
      justify-content: center;
      padding: 2rem;
    }

    .profile-grid {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 2rem;
      width: 100%;
    }

    .profile-card {
      background: white;
      border-radius: 24px;
      padding: 1.5rem;
      width: 150px;
      height: 170px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 1rem;
      cursor: pointer;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
      transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      border: 3px solid transparent;
      outline: none;
      position: relative;
      overflow: hidden;
    }

    .profile-card:hover, .profile-card:focus {
      transform: translateY(-8px) scale(1.02);
      box-shadow: 0 20px 40px rgba(0, 210, 180, 0.2);
      border-color: #00e676;
    }

    .avatar-circle {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      background: #e0f2f1;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #009688;
      transition: all 0.3s ease;
      font-size: 2.5rem;
    }
    
    .profile-card:hover .avatar-circle {
      background-color: #b9f6ca;
      transform: scale(1.1);
    }
    
    /* Create Card Styles */
    .create-card {
      background: rgba(255, 255, 255, 0.5);
      border: 3px dashed #b0bec5;
      box-shadow: none;
    }
    
    .create-card:hover {
      background: rgba(255, 255, 255, 0.9);
      border-color: #00e676;
      border-style: solid;
      box-shadow: 0 10px 30px rgba(0, 230, 118, 0.2);
    }
    
    .create-circle {
      background: #eceff1;
      color: #90a4ae;
    }
    
    .create-card:hover .create-circle {
      background: #b9f6ca;
      color: #00c853;
      transform: rotate(90deg);
    }

    mat-icon {
      transform: scale(1.5);
    }

    .profile-name {
      font-weight: 700;
      color: #37474f;
      text-align: center;
      font-size: 1.1rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
    }

    .emoji-avatar {
        line-height: 1;
        display: block;
        padding-top: 4px; /* Slight adjustment for emoji vertical alignment */
    }
  `]
})
export class SelectProfileComponent implements OnInit {
  readonly profiles = signal<Profile[]>([]);
  readonly loading = signal(false);

  // Animal emojis for profiles
  readonly animalEmojis = ['🐻', '🦁', '🐯', '🐨', '🐼', '🦊', '🐰', '🐹', '🐶', '🐱', '🐸', '🐙', '🦄', '🐲', '🦉', '🦜', '🦝', '🐗'];

  constructor(
    private readonly profileService: ProfileService,
    private readonly router: Router
  ) { }

  ngOnInit(): void {
    this.createProfileIfNone();
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
