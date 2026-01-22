---
name: write-effective-pull-requests
description: Create comprehensive pull requests that streamline code review and context.
---

# Writing Effective Pull Requests

## Overview

A Pull Request (PR) is not just a collection of code changes; it is a communication tool. A well-written PR provides the "Why" and "What" to the reviewer, ensuring they can verify correctness and intent without needing to read every line of code. This skill focuses on creating PRs that are easy to triage, review, and merge.

## Title Standards

Use the **Conventional Commits** specification for the PR title. This allows automation to link the PR to changelogs and issue trackers.

**Format:** `<type>(<scope>): <subject>`

*   **feat:** A new feature
*   **fix:** A bug fix
*   **refactor:** Code changes that neither fix a bug nor add a feature
*   **docs:** Documentation only changes
*   **test:** Adding or updating tests
*   **chore:** Maintenance tasks (dependencies, build config)

**Examples:**
*   `feat(auth): add OAuth2 login support`
*   `fix(api): handle null pointer on user fetch`
*   `docs(readme): update installation instructions`

## Standard Description Template

Always use this structure to ensure consistency. Fill out every relevant section.

```markdown
## Context & Motivation
Explain *why* this change is happening. Reference any specific design docs or user feedback.
- What problem does this solve?
- Why was this approach chosen over alternatives?

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Refactoring (improving code structure without changing behavior)

## Changes Made
Use bullet points to describe high-level changes. Do not just list filenames.
- Implemented X service to handle Y logic
- Updated Z component to include new props
- Added unit tests for edge cases

## Related Issues
Link to any related tickets.
- Resolves #123
- Relates to #456

## Testing Performed
Describe how you verified the code works.
- Manual testing steps (e.g., "Clicked button A, saw result B")
- Unit test results (e.g., "npm test passed")
- Screenshots (if UI changes occurred)

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

## Critical Guidelines

### 1. The "Context" Rule
Never assume the reviewer knows the background. If a user reported a bug, summarize the user scenario. If this is a refactor, explain the technical debt being addressed.

### 2. Linking Issues
Always link the PR to the corresponding issue using keywords like `Resolves`, `Fixes`, or `Closes` followed by the issue number. This ensures the issue closes automatically upon merge.

### 3. Visual Proof
If your change touches the UI, **you must include screenshots or recordings**. Reviewers should not have to pull the branch locally to see if a button moved 2 pixels to the left.

### 4. Scope Control
A PR should focus on a single task. If you find yourself adding unrelated fixes (e.g., fixing a typo while implementing a feature), create a separate PR. "Kitchen sink" PRs are difficult to review and dangerous to merge.

### 5. Breaking Changes
If a PR introduces a breaking change, you must explicitly mark it in the description and provide a **Migration Guide** explaining how users should update their code or workflows.

## Common Pitfalls

*   **Vague Titles:** Avoid titles like "Update file" or "WIP". Be specific.
*   **Missing Context:** "Fixed it" is not a context. Explain what "it" was and how it was broken.
*   **Incomplete Checklist:** Do not check the testing box if you only manually clicked around once. Ensure unit tests cover the new logic.
*   **Leftover Debug Code:** Never submit `console.log`, `debugger`, or commented-out code blocks. Clean your diffs before opening the PR.