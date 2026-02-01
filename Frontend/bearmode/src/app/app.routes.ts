import { Routes } from '@angular/router';
import { AppLayoutComponent } from './layout/app-layout.component';
import { ManageProfileComponent } from './pages/manage-profile/manage-profile.component';
import { StartScreenComponent } from './pages/start-screen/start-screen.component';

export const routes: Routes = [
  {
    path: '',
    component: AppLayoutComponent,
    children: [
      { path: '', component: StartScreenComponent },
      { path: 'manage-profile', component: ManageProfileComponent }
    ]
  },
  { path: '**', redirectTo: '' }
];
