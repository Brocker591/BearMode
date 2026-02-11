import { Component, OnInit, signal, computed, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { TrainingPlanService } from '../../../services/training-plan.service';
import type { TrainingPlanExecuteResponse, TrainingExerciseExecuteResponse } from '../../../models/training-plan';
import { TimerFinishedDialogComponent } from '../../../components/timer-finished-dialog/timer-finished-dialog.component';

@Component({
    selector: 'app-training-execute-session',
    standalone: true,
    imports: [
        CommonModule,
        MatTableModule,
        MatButtonModule,
        MatIconModule,
        MatDialogModule
    ],
    templateUrl: './training-execute-session.component.html',
    styleUrls: ['./training-execute-session.component.css']
})
export class TrainingExecuteSessionComponent implements OnInit, OnDestroy {
    plan = signal<TrainingPlanExecuteResponse | null>(null);
    loading = signal(true);
    error = signal<string | null>(null);

    // Timer properties
    readonly timerValue = signal<number>(0);
    readonly timerRunning = signal<boolean>(false);

    dataSource = new MatTableDataSource<TrainingExerciseExecuteResponse>([]);
    displayedColumns: string[] = ['order', 'description', 'sets_info', 'break_time', 'video'];

    private timerInterval: any;
    private audioContext: AudioContext | null = null;
    private oscillator: OscillatorNode | null = null;

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private trainingPlanService: TrainingPlanService,
        private dialog: MatDialog
    ) { }

    ngOnInit(): void {
        const planId = this.route.snapshot.paramMap.get('id');
        if (!planId) {
            this.error.set('Keine Plan-ID gefunden.');
            this.loading.set(false);
            return;
        }

        this.loadPlan(planId);
    }

    ngOnDestroy(): void {
        this.stopTimer();
        this.stopAlarm();
    }

    // Timer Logic
    readonly formattedTime = computed(() => {
        const totalSeconds = this.timerValue();
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    });

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
        this.timerValue.update(v => v + seconds);
    }

    timerFinished() {
        this.pauseTimer();
        this.playAlarm();
        this.openAlarmDialog();
    }

    // Alarm Logic (AudioContext)
    playAlarm() {
        try {
            this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
            this.oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            this.oscillator.type = 'square';
            this.oscillator.frequency.setValueAtTime(440, this.audioContext.currentTime); // A4
            this.oscillator.frequency.exponentialRampToValueAtTime(880, this.audioContext.currentTime + 0.1);

            // Beeping effect
            const now = this.audioContext.currentTime;
            gainNode.gain.setValueAtTime(0.5, now);
            gainNode.gain.setValueAtTime(0, now + 0.5);
            gainNode.gain.setValueAtTime(0.5, now + 1);
            gainNode.gain.setValueAtTime(0, now + 1.5);
            gainNode.gain.setValueAtTime(0.5, now + 2);
            gainNode.gain.setValueAtTime(0, now + 2.5);

            this.oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            this.oscillator.start();
            // Stop automatically after some time if not handled? 
            // Better to loop until dialog closed.
            // Let's make it a continuous loop for now or simple long beep pattern.
            // Simple approach: Beep-Beep-Beep... handled by manually stopping oscillator.
            // Actually, let's just make it loop.
            this.oscillator.onended = () => this.stopAlarm();
        } catch (e) {
            console.error('AudioContext error', e);
        }
    }

    stopAlarm() {
        if (this.oscillator) {
            try {
                this.oscillator.stop();
                this.oscillator.disconnect();
            } catch (e) { }
            this.oscillator = null;
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

    loadPlan(id: string) {
        this.loading.set(true);
        this.trainingPlanService.getExecutePlan(id).subscribe({
            next: (data) => {
                this.plan.set(data);
                this.dataSource.data = data.exercises;
                this.loading.set(false);
            },
            error: (err: any) => {
                console.error('Error loading execution plan', err);
                this.error.set('Fehler beim Laden des Plans.');
                this.loading.set(false);
            }
        });
    }

    goBack() {
        this.router.navigate(['/training-execute']);
    }

    openVideo(url: string | null | undefined) {
        if (url) {
            window.open(url, '_blank');
        }
    }
}
