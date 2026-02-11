import { Routes } from '@angular/router';
import { AppLayoutComponent } from './layout/app-layout.component';
import { ManageProfileComponent } from './pages/manage-profile/manage-profile.component';
import { StartScreenComponent } from './pages/start-screen/start-screen.component';
import { TrainingExerciseItemComponent } from './pages/training-exercise-item/training-exercise-item';
import { TrainingPlanPageComponent } from './pages/training-plan-page/training-plan-page.component';
import { SelectProfileComponent } from './pages/select-profile/select-profile.component';
import { TrainingExecuteListComponent } from './pages/training-execute/training-execute-list/training-execute-list.component';
import { TrainingExecuteSessionComponent } from './pages/training-execute/training-execute-session/training-execute-session.component';
import { profileGuard } from './guards/profile.guard';

export const routes: Routes = [
  {
    path: 'select-profile',
    component: SelectProfileComponent // No layout or different layout? Assuming standalone page for now or with layout?
  },
  {
    path: '',
    component: AppLayoutComponent,
    children: [
      { path: '', component: StartScreenComponent, canActivate: [profileGuard] },
      { path: 'manage-profile', component: ManageProfileComponent, canActivate: [profileGuard] },
      { path: 'training-exercise-item', component: TrainingExerciseItemComponent, canActivate: [profileGuard] },
      { path: 'training-plans', component: TrainingPlanPageComponent, canActivate: [profileGuard] },
      { path: 'training-execute', component: TrainingExecuteListComponent, canActivate: [profileGuard] },
    ]
  },
  {
    path: 'training-execute/:id',
    component: TrainingExecuteSessionComponent,
    canActivate: [profileGuard]
  },
  { path: '**', redirectTo: '' }
];
