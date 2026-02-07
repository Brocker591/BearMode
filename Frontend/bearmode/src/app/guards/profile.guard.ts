
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
    // Allow access to select-profile
    if (targetUrl.includes('select-profile')) {
        return true;
    }

    // Allow access to manage-profile ONLY if creating a new profile
    if (targetUrl.includes('manage-profile')) {
        const urlTree = router.parseUrl(targetUrl);
        if (urlTree.queryParams['create'] === 'true') {
            return true;
        }
    }

    // Otherwise redirect to select-profile
    return router.createUrlTree(['/select-profile']);
};
