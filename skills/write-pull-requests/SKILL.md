---
name: write-pull-requests
description: Create comprehensive Pull Request descriptions with context, testing evidence, and checklists.
---

# Writing Effective Pull Requests

## Overview

A Pull Request (PR) is more than a diff; it is a narrative that explains intent. A good PR allows reviewers to understand the change without needing to reverse-engineer the code. This guide ensures descriptions contain the necessary context, testing details, and formatting to facilitate smooth reviews.

## PR Titles

Use the Conventional Commits format for titles to ensure consistency.
- **Style:** Imperative mood ("Add" not "Added").
- **Format:** `<type>(<scope>): <subject>`
- **Types:** feat, fix, docs, refactor, test, chore.

## PR Description Structure

Every PR must include the following sections. This prevents "silent" changes that are difficult to review.

### 1. Summary & Motivation
- **Summary:** One or two sentences describing the change.
- **Why:** Link to the related issue (e.g., `Closes #123`). Explain the business or technical reason for the change.

### 2. Technical Changes
- Detail the technical approach. Did you change a database schema? Update an API schema?
- Mention any trade-offs made.

### 3. Testing & Verification
- Prove the code works. Do not just say "It works."
- Include reproduction steps for bugs or screenshots for UI changes.

### 4. Checklist
Include a standard list to ensure quality gates are met:
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Linter passing

## Examples

### Feature Implementation
```markdown
## Summary
Implement OAuth2 login with Google provider.

## Motivation
Users have requested a password-less login option. 
Reduces friction for onboarding. 
Related ticket: #456

## Changes
- Added `google-auth` library.
- Created `/auth/google/callback` endpoint.
- Updated user model to store OAuth provider ID.

## Testing
- Verified redirect loop to Google.
- Tested user creation flow upon first login.
- Verified existing account linking.
- [x] Unit tests for callback handler
- [x] Manual QA in staging environment
```

### Bug Fix
```markdown
## Summary
Fix race condition in order processing pipeline.

## Root Cause
Two workers were picking up the same job due to missing locking in Redis.
This caused duplicate invoice generation.

## Fix
Implemented `redlock` strategy on the `process_order` job.
Added `order_id` unique constraint on invoices table as a safeguard.

## Testing
- Reproduced the race condition locally using a concurrency script.
- Verified the fix prevents double-processing under load.
- [x] Regression tests for existing orders
```

## Common Pitfalls to Avoid

1. **"Mega-PRs":** Keep changes small and focused. If a PR exceeds 400 lines, consider splitting it.
2. **Vague Context:** Never assume the reviewer knows the background. Always link an issue.
3. **Missing Screenshots:** For CSS/UI changes, always provide "Before" and "After" screenshots.
4. **Ignoring Review Comments:** Do not push new commits without addressing outstanding questions first.