import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartData, ChartType } from 'chart.js';
import { TrainingPlanService } from '../../services/training-plan.service';
import { ProfileService } from '../../services/profile.service';
import { TrainingExerciseCompletion } from '../../models/training-plan';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  private trainingPlanService = inject(TrainingPlanService);
  private profileService = inject(ProfileService);

  // Stats
  totalExercisesCompleted = signal(0);
  exercisesThisWeek = signal(0);
  favoriteExercise = signal<string>('-');

  // Weekly Chart Data
  public weeklyChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Übungen pro Tag (letzte 7 Tage)' }
    }
  };
  public weeklyChartType: ChartType = 'bar';
  public weeklyChartData: ChartData<'bar'> = {
    labels: [],
    datasets: [
      { data: [], label: 'Übungen', backgroundColor: '#3b82f6' }
    ]
  };

  // Top Exercises Chart Data
  public topExercisesChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'right' },
      title: { display: true, text: 'Top 5 Übungen' }
    }
  };
  public topExercisesChartType: ChartType = 'doughnut';
  public topExercisesChartData: ChartData<'doughnut'> = {
    labels: [],
    datasets: [
      {
        data: [],
        backgroundColor: [
          '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6'
        ]
      }
    ]
  };

  ngOnInit() {
    const profile = this.profileService.selectedProfile();
    if (profile) {
      this.loadData(profile.id);
    }
  }

  loadData(profileId: string) {
    this.trainingPlanService.getCompletionHistory(profileId).subscribe({
      next: (data) => this.processData(data),
      error: (err) => console.error('Failed to load history', err)
    });
  }

  processData(data: TrainingExerciseCompletion[]) {
    this.totalExercisesCompleted.set(data.length);

    // Calculate Weekly Stats (Last 7 days)
    const today = new Date();
    const lastWeek = new Date(today);
    lastWeek.setDate(today.getDate() - 6); // inclusive today = 7 days

    const dailyCounts: { [key: string]: number } = {};
    const labels: string[] = [];

    // Initialize map and labels for last 7 days
    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setDate(today.getDate() - i);
      const dateStr = d.toISOString().split('T')[0];
      dailyCounts[dateStr] = 0;
      labels.push(d.toLocaleDateString('de-DE', { weekday: 'short', day: '2-digit', month: '2-digit' }));
    }

    let thisWeekCount = 0;

    // Top Exercises
    const exerciseCounts: { [key: string]: number } = {};

    data.forEach(item => {
      // Assuming training_day exists, otherwise use a fallback or current date if newly created?
      // Backend schema says training_day: date | None. If None, skip?
      if (item.training_day) {
        const itemDate = new Date(item.training_day).toISOString().split('T')[0];

        // Weekly count
        if (dailyCounts.hasOwnProperty(itemDate)) {
          dailyCounts[itemDate]++;
          thisWeekCount++;
        }
      }

      // Exercise frequency
      const name = item.exercise_description;
      exerciseCounts[name] = (exerciseCounts[name] || 0) + 1;
    });

    this.exercisesThisWeek.set(thisWeekCount);

    // Update Weekly Chart
    this.weeklyChartData = {
      labels: labels,
      datasets: [{
        data: Object.values(dailyCounts),
        label: 'Übungen',
        backgroundColor: '#3b82f6',
        borderRadius: 4
      }]
    };

    // Update Top Exercises Chart
    const sortedExercises = Object.entries(exerciseCounts)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5);

    if (sortedExercises.length > 0) {
      this.favoriteExercise.set(`${sortedExercises[0][0]} (${sortedExercises[0][1]}x)`);

      this.topExercisesChartData = {
        labels: sortedExercises.map(([name]) => name),
        datasets: [{
          data: sortedExercises.map(([, count]) => count),
          backgroundColor: [
            '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6'
          ],
          hoverOffset: 4
        }]
      };
    }
  }
}
