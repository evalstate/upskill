---
name: writing-pull-requests
description: Create comprehensive PR descriptions including context, impact, and testing instructions.
---

# Writing Pull Requests

## Overview

A high-quality Pull Request (PR) description serves as the historical record of a change and enables efficient code reviews. Agents must clearly explain the *context*, the *impact*, and the *verification* steps, avoiding generic or vague summaries.

## Key Principles

1.  **Context First:** Explain "Why" before "What". Link to relevant tickets (e.g., `Fixes #123`).
2.  **Coherent Summaries:** Group changes logically (e.g., "Updated API," "Fixed UI bug") rather than listing every file touched.
3.  **Impact Awareness:** Explicitly state if the change introduces breaking changes, performance implications, or requires database migrations.
4.  **Visibility:** If the PR touches the UI, a screenshot or screen recording is mandatory.

## PR Structure

Use this template to ensure all critical information is present:

```markdown
## Summary
[One sentence explaining what the PR does.]

## Context / Motivation
[Why is this change necessary? What problem does it solve?]

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Docs / Refactoring / Code style

## Changes Detailed
- Update X to handle Y
- Remove deprecated Z endpoint
- Add visual indicator for selection state

## Testing & Reproduction
[How to verify the fix or test the feature]

## Checklist
- [ ] Code compiles and builds pass
- [ ] Unit/Integration tests added/updated
- [ ] Documentation updated
```

## Examples

### Bug Fix (UI Focused)
```markdown
## Summary
Fixes the alignment issue on the mobile navigation bar.

## Context
Users on iOS Safari reported that the "Login" button was obscured by the status bar.
Related issue: #405

## Changes
- Increased padding-top on `.nav-container` to safe-area-inset.
- Added media query for devices with width < 768px.

## Testing
1. Open Safari on an iOS device.
2. Navigate to the home page.
3. Verify the "Login" button is fully visible and clickable.

## Visuals
[Attach screenshot of fixed mobile view]
```

### Breaking Change (Backend)
```markdown
## Summary
Updates the `/users` endpoint to return ISO 8601 date strings.

## Context
The frontend team standardizing on date formats. This changes the backend response to match the new contract.

## Breaking Changes
The `created_at` field previously returned timestamps (integers). It now returns strings (e.g., "2023-10-12T10:00:00Z"). Frontend consumers must update their date parsing logic.

## Testing
- Run integration tests `test_api_v2`.
- Verify legacy clients fail as expected and log clear error messages.
```

## Best Practices

- **Be Concise:** Don't copy-paste the code diff into the description.
- **Flag WIPs:** If the PR is a Work In Progress, prefix the title with `[WIP]`.
- **Co-author Credit:** If you adapted code from elsewhere, use the `Co-authored-by:` trailer in the commit message or PR body.