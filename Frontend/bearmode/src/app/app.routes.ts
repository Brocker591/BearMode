import { Routes } from '@angular/router';
import { AppLayoutComponent } from './layout/app-layout.component';
import { ManageProfileComponent } from './pages/manage-profile/manage-profile.component';
import { StartScreenComponent } from './pages/start-screen/start-screen.component';
import { TrainingExerciseItemComponent } from './pages/training-exercise-item/training-exercise-item';
import { TrainingPlanPageComponent } from './pages/training-plan-page/training-plan-page.component';

export const routes: Routes = [
  {
    path: '',
    component: AppLayoutComponent,
    children: [
      { path: '', component: StartScreenComponent },
      { path: 'manage-profile', component: ManageProfileComponent },
      { path: 'training-exercise-item', component: TrainingExerciseItemComponent },
      { path: 'training-plans', component: TrainingPlanPageComponent }
    ]
  },
  { path: '**', redirectTo: '' }
];
