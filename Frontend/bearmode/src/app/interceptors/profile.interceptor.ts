
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

export const profileInterceptor: HttpInterceptorFn = (req, next) => {
    // Read from localStorage directly to avoid strict circular dependency with ProfileService
    // if ProfileService also depends on HttpClient.
    // Although in modern Angular with functional interceptors and providedIn: root, it might be handled,
    // reading from localStorage is robust here since ProfileService syncs to it.

    // Skip adding header for profile management endpoints to avoid issues
    if (req.url.includes('/profiles')) {
        return next(req);
    }

    const savedProfile = localStorage.getItem('selectedProfile');
    if (savedProfile) {
        try {
            const profile = JSON.parse(savedProfile);
            if (profile && profile.id) {
                const clonedReq = req.clone({
                    headers: req.headers.set('X-Profile-Id', profile.id)
                });
                return next(clonedReq);
            }
        } catch (e) {
            // Ignore parse error
        }
    }

    return next(req);
};
