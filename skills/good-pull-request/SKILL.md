---
name: good-pull-request
description: Teach AI to write clear, concise, and effective pull request titles and descriptions.
---

# Writing a Good Pull Request (PR)

## Overview
A well‑crafted PR communicates **what** changed, **why** it changed, and **how** the reviewer can validate it. Clear PRs reduce back‑and‑forth, speed up merges, and improve project documentation.

## Key Principles

| Principle | Details |
|-----------|---------|
| **Descriptive Title** | ≤ 72 characters, use imperative mood (`Add`, `Fix`, `Update`). Include scope if helpful (`ui:`, `api:`). |
| **Why, Not Just What** | Explain the motivation, related tickets, and expected impact. |
| **Minimal Scope** | Keep PRs focused on a single logical change. Split large work into multiple PRs. |
| **Evidence** | Add screenshots, logs, or test results that prove the change works. |
| **Checklist** | Provide a short list (e.g., tests run, docs updated) for reviewers to verify. |
| **Link Issues** | Use keywords (`Closes #123`, `Related to #456`) so the issue tracker auto‑updates. |

## Step‑by‑Step Guide

1. **Craft the Title**  
   - Format: `<type>(<scope>): <short description>`  
   - Example: `feat(auth): add password‑reset endpoint`

2. **Write the Body**  
   - **Motivation**: One‑paragraph why the change is needed.  
   - **Solution**: Summarize what was done (no line‑by‑line code dump).  
   - **Testing**: Describe how you verified the change (unit tests, manual steps).  
   - **Impact**: Note any breaking changes or migrations required.

3. **Add a Checklist** (optional but recommended)  
   ```markdown
   - [x] Unit tests added / updated  
   - [x] Documentation updated  
   - [x] Linting passes  
   - [x] Manual testing performed on dev environment
   ```

4. **Link Issues** using GitHub keywords (`Closes #42`).  

## Example PR

### Title
```
fix(api): handle null user response in login endpoint
```

### Description
```
**Why**  
The login endpoint crashes when the user service returns `null`, causing a 500 error for callers.

**What**  
Added a null‑check before accessing user fields and returned a 404 with a friendly message when the user is not found.

**Testing**  
- Added unit test `test_login_user_not_found` covering the null case.  
- Ran integration test against staging; all 10 login scenarios passed.

**Impact**  
No breaking API changes; existing clients receive a proper 404 instead of 500.

Closes #78
```

### Checklist
```
- [x] Unit tests cover new null‑check
- [x] Updated API docs with 404 response
- [x] Linting passes
- [x] Verified on local dev server
```

## Best Practices & Pitfalls
- **Avoid vague titles** like “Fix bugs” – be specific.  
- **Don’t include full diffs**; the code view handles that.  
- **Keep the description focused**; extraneous background can drown the signal.  
- **Remember the reviewer**: assume they are busy and need to understand quickly.  
- **Update the PR** if feedback reveals missing information – treat it as a living document.