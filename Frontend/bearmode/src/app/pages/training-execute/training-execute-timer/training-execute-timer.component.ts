import { Component, computed, signal, OnDestroy, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { TimerFinishedDialogComponent } from '../../../components/timer-finished-dialog/timer-finished-dialog.component';

@Component({
    selector: 'app-training-execute-timer',
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        MatButtonModule,
        MatIconModule,
        MatTooltipModule,
        MatDialogModule,
        MatFormFieldModule,
        MatInputModule
    ],
    templateUrl: './training-execute-timer.component.html',
})
export class TrainingExecuteTimerComponent implements OnDestroy {
    @Input() planName: string | undefined;

    // Timer properties
    readonly timerValue = signal<number>(0);
    readonly timerRunning = signal<boolean>(false);

    // Manual Input properties
    readonly inputMinutes = signal<number | null>(null);
    readonly inputSeconds = signal<number | null>(null);

    readonly formattedTime = computed(() => {
        const totalSeconds = this.timerValue();
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    });

    private timerInterval: any;
    private audioContext: AudioContext | null = null;
    private oscillator: OscillatorNode | null = null;

    constructor(private dialog: MatDialog, private router: Router) { }

    ngOnDestroy(): void {
        this.stopTimer();
        this.stopAlarm();
    }

    setTimerFromInput() {
        const mins = this.inputMinutes() || 0;
        const secs = this.inputSeconds() || 0;
        if (mins >= 0 && secs >= 0 && (mins > 0 || secs > 0)) {
            this.pauseTimer();
            this.timerValue.set(mins * 60 + secs);
            // Optional: Clear inputs after setting? 
            // this.inputMinutes.set(null);
            // this.inputSeconds.set(null);
        }
    }

    // Timer Logic
    startTimer() {
        if (this.timerValue() <= 0) return;

        this.pauseTimer(); // Clear any existing interval
        this.timerRunning.set(true);

        this.timerInterval = setInterval(() => {
            const current = this.timerValue();
            if (current > 0) {
                this.timerValue.set(current - 1);
            } else {
                this.timerFinished();
            }
        }, 1000);
    }

    pauseTimer() {
        this.timerRunning.set(false);
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    stopTimer() { // Acts as reset/clear
        this.pauseTimer();
        this.timerValue.set(0);
    }

    addTime(seconds: number) {
        this.timerValue.update((v: number) => v + seconds);
    }

    timerFinished() {
        this.pauseTimer();
        this.playAlarm();
        this.openAlarmDialog();
    }

    private alarmInterval: any;

    // Alarm Logic (AudioContext)
    playAlarm() {
        try {
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
            }

            // Start repeating beep pattern
            this.playBeepSequence(); // Play immediately first time
            this.alarmInterval = setInterval(() => {
                this.playBeepSequence();
            }, 1000);

        } catch (e) {
            console.error('AudioContext error', e);
        }
    }

    playBeepSequence() {
        if (!this.audioContext) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.type = 'square';
        oscillator.frequency.value = 880; // A5 - Classic alarm pitch

        const now = this.audioContext.currentTime;

        // Pattern: Beep (0.1s) - Pause (0.1s) - Beep (0.1s)
        gainNode.gain.setValueAtTime(0, now);

        // First Beep
        gainNode.gain.linearRampToValueAtTime(0.5, now + 0.01);
        gainNode.gain.setValueAtTime(0.5, now + 0.1);
        gainNode.gain.linearRampToValueAtTime(0, now + 0.11);

        // Second Beep
        gainNode.gain.linearRampToValueAtTime(0.5, now + 0.21);
        gainNode.gain.setValueAtTime(0.5, now + 0.3);
        gainNode.gain.linearRampToValueAtTime(0, now + 0.31);

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.start(now);
        oscillator.stop(now + 0.4); // Stop after sequence
    }

    stopAlarm() {
        if (this.alarmInterval) {
            clearInterval(this.alarmInterval);
            this.alarmInterval = null;
        }

        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
    }

    openAlarmDialog() {
        const dialogRef = this.dialog.open(TimerFinishedDialogComponent, {
            width: '400px',
            disableClose: true
        });

        dialogRef.afterClosed().subscribe(() => {
            this.stopAlarm();
        });
    }

    goBack() {
        this.router.navigate(['/training-execute']);
    }
}
