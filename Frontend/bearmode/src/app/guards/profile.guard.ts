
import { inject } from '@angular/core';
import { Router, type CanActivateFn } from '@angular/router';
import { ProfileService } from '../services/profile.service';

export const profileGuard: CanActivateFn = (route, state) => {
    const profileService = inject(ProfileService);
    const router = inject(Router);

    if (profileService.selectedProfile()) {
        return true;
    }

    const targetUrl = state.url;
    // Allow access to select-profile and manage-profile even without a selected profile
    if (targetUrl.includes('select-profile') || targetUrl.includes('manage-profile')) {
        return true;
    }

    // Otherwise redirect to select-profile
    return router.createUrlTree(['/select-profile']);
};
