import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
    selector: 'app-timer-finished-dialog',
    standalone: true,
    imports: [MatDialogModule, MatButtonModule, MatIconModule],
    template: `
    <h2 mat-dialog-title class="text-center text-red-600">
      <mat-icon class="align-bottom text-4xl">timer_off</mat-icon>
      Zeit abgelaufen!
    </h2>
    <mat-dialog-content class="text-center">
      <p class="text-lg">Die eingestellte Ruhezeit ist vorbei.</p>
    </mat-dialog-content>
    <mat-dialog-actions align="center">
      <button mat-flat-button color="warn" (click)="onClose()" class="w-full text-lg py-2">
        <mat-icon>stop</mat-icon> Alarm stoppen
      </button>
    </mat-dialog-actions>
  `,
    styles: [`
    mat-icon {
       vertical-align: middle;
    }
  `]
})
export class TimerFinishedDialogComponent {
    constructor(
        public dialogRef: MatDialogRef<TimerFinishedDialogComponent>,
        @Inject(MAT_DIALOG_DATA) public data: any
    ) { }

    onClose(): void {
        this.dialogRef.close();
    }
}
