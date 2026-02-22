import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { DataSyncService } from '../../services/data-sync.service';

@Component({
    selector: 'app-data-sync',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './data-sync.component.html',
})
export class DataSyncComponent {
    private dataSyncService = inject(DataSyncService);
    private router = inject(Router);

    isExporting = false;
    isImporting = false;
    importError: string | null = null;
    importSuccess = false;

    exportData() {
        this.isExporting = true;
        this.dataSyncService.exportData().subscribe({
            next: (data) => {
                const json = JSON.stringify(data, null, 2);
                const blob = new Blob([json], { type: 'application/json' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                const date = new Date().toISOString().split('T')[0];
                a.download = `bearmode-export-${date}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                this.isExporting = false;
            },
            error: (err) => {
                console.error('Error exporting data', err);
                this.isExporting = false;
            }
        });
    }

    onFileSelected(event: any) {
        this.importError = null;
        this.importSuccess = false;
        const file: File = event.target.files[0];

        if (file) {
            this.isImporting = true;
            const reader = new FileReader();

            reader.onload = (e: any) => {
                try {
                    const content = e.target.result;
                    const parsedData = JSON.parse(content);

                    this.dataSyncService.importData(parsedData).subscribe({
                        next: (res) => {
                            this.importSuccess = true;
                            this.isImporting = false;
                            event.target.value = ''; // Reset file input
                            setTimeout(() => {
                                this.router.navigate(['/select-profile']).then(() => {
                                    window.location.reload(); // optionally reload to ensure all state is cleared
                                });
                            }, 1500);
                        },
                        error: (err) => {
                            console.error('Error importing data', err);
                            this.importError = 'Fehler beim Importieren der Daten. Bitte prüfen Sie die Konsolenausgabe für Details.';
                            this.isImporting = false;
                            event.target.value = '';
                        }
                    });
                } catch (error) {
                    console.error('Error parsing JSON', error);
                    this.importError = 'Die Datei entält kein gültiges JSON Format.';
                    this.isImporting = false;
                    event.target.value = '';
                }
            };

            reader.onerror = () => {
                this.importError = 'Fehler beim Lesen der Datei.';
                this.isImporting = false;
            };

            reader.readAsText(file);
        }
    }
}
