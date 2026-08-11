# PWA

The production response advertises `/manifest.webmanifest`, theme color `#070708`, an Apple touch icon, and standalone-capable metadata. Full service-worker/install/offline/update behavior is not yet verified.

Acceptance requires a valid manifest (name, short name, start URL, display, theme/background colors, maskable icons), HTTPS, registered service worker, installability audit, safe cache scope, no caching of authenticated/private API responses, offline/error UX, update notification, and installed launch on iPhone and Android. Test the canonical production build—not the legacy Next.js implementation.
