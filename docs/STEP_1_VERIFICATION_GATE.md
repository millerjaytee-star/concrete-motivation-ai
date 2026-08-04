# Step 1 Verification Gate

Step 1 remains provisional until the independent web foundation passes every required check on GitHub Actions.

## Required automated checks

- Clean dependency installation on Node.js 22
- TypeScript strict typecheck
- Next.js production build
- No missing dependency or lockfile assumptions in CI

## Required manual review before Step 2

- Homepage renders at 320px, tablet, and desktop widths
- Keyboard navigation and visible focus states work
- Skip link reaches the main content
- Reduced-motion preference is respected
- Public navigation contains no authentication gate
- Every configured link has a safe default
- No fake testimonials, metrics, clients, partners, or social proof

## Merge policy

Future feature branches follow this sequence:

1. Build
2. Test
3. Inspect
4. Fix
5. Retest
6. Owner review when applicable
7. Merge

A merge is not considered verified merely because GitHub accepted it.
