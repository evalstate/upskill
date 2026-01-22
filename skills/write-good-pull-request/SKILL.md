---
name: write-good-pull-request
description: Create clear, comprehensive pull requests that facilitate effective code review.
---

# Writing Effective Pull Requests

## Overview

A well-crafted pull request (PR) accelerates code review, reduces back-and-forth discussions, and maintains project history. This guide covers the essential elements of creating PRs that reviewers appreciate.

## PR Structure

### Title Format
```
<type>: Brief description (50 chars max)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Description Template
```markdown
## Summary
Brief explanation of what changed and why.

## Changes
- Specific change 1
- Specific change 2

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if UI changes)
// Before/after images

## Related Issues
Closes #123
```

## Best Practices

### 1. Keep PRs Small
- Focus on a single feature or fix
- Maximum ~400 lines of changes
- Split large refactors into multiple PRs

### 2. Write Self-Review Comments
```python
# Added timeout to prevent hanging requests
response = requests.get(url, timeout=30)
```

### 3. Update Documentation
```markdown
## API Changes
- Added new endpoint `/api/v2/users`
- Updated OpenAPI spec
- Added example to README
```

### 4. Include Test Evidence
```bash
# Run tests and include output
pytest tests/test_new_feature.py -v
=== 5 passed, 0 failed ===
```

## Reviewer Checklist

Before submitting, verify:
- [ ] PR title follows convention
- [ ] Description is complete
- [ ] Tests are included
- [ ] Documentation updated
- [ ] No debugging code remains
- [ ] Commit messages are clean

## Common Mistakes to Avoid

- **Vague titles**: "Fix bug" → "Fix null pointer in user service"
- **Missing context**: Always explain the problem being solved
- **Large PRs**: Break into smaller, reviewable chunks
- **No test plan**: Always specify how changes were tested