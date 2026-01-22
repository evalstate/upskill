---
name: effective-pull-requests
description: Write clear, structured Pull Request descriptions that provide context and facilitate review.
---

# Effective Pull Requests

## Overview

A well-written Pull Request (PR) bridges the gap between code and intent. The goal is to minimize reviewer cognitive load by providing the "why" and "what" before they ever look at the code. A good PR ensures that changes are safe, tested, and valuable.

## Standard Template

Use this structure for every PR. Filling out every section reduces review time and prevents deployment issues.

```markdown
## 📋 Summary
[One sentence explaining the high-level goal of this change.]

## 🎯 Motivation & Context
[Why is this change necessary? Link to related tickets (e.g., Resolves #123).]

## 🛠️ Changes
- [High-level bullet point describing major change 1]
- [High-level bullet point describing major change 2]
- [Technical detail regarding implementation approach, if necessary]

## 🧪 Testing
[How did you verify this works? e.g., "Added unit test X", "Manual QA on feature flag Y"]

## 📦 Deployment Notes
[Any critical info for Ops/Deploy. e.g., DB migrations, breaking changes, env vars needed.]

## ✅ Checklist
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new linting errors
```

## Examples

### Feature PR with Deployment Implications
## 📋 Summary
Integrate Stripe payments for subscription upgrades.

## 🎯 Motivation & Context
Users cannot currently upgrade to Pro plans automatically. Relates to Ticket #45.

## 🛠️ Changes
- Added `StripeService` to handle payment intents.
- Updated `SubscriptionController` with new `/upgrade` endpoint.
- Added UI modal for credit card input.

## 🧪 Testing
- Manual test: Completed full payment flow using Stripe test keys.
- Unit tests: Covered success scenarios and card declined errors.

## 📦 Deployment Notes
- **Migration Required:** `003_add_stripe_customer_id.sql` must run before code deployment.
- **Env Vars:** `STRIPE_SECRET_KEY` must be set in production.

### Bug Fix PR
## 📋 Summary
Fix memory leak in WebSocket connection handler.

## 🎯 Motivation & Context
Server memory usage increases by 10% every hour under heavy load due to unclosed event listeners. Issue #892.

## 🛠️ Changes
- Wrapped event listeners in a `try/finally` block to ensure cleanup.
- Added `max_connections` limit to the config.

## 🧪 Testing
- Ran load test simulating 1,000 concurrent connections; memory usage remained stable.

## Best Practices

1.  **Explain the "Why"**: Don't just list changed files. Explain the business logic or technical debt being addressed.
2.  **Keep PRs Small**: Large PRs (500+ lines) are rarely reviewed thoroughly. Break complex features into smaller, iterative PRs.
3.  **Call Out Breaking Changes**: If this PR deletes an API endpoint or changes a data contract, make it the first thing in the description.
4.  **Use Visuals**: For UI changes, include screenshots or screen recordings. A picture is worth a thousand lines of CSS.

## Common Pitfalls to Avoid

*   **Vague Titles**: Avoid titles like "Update files" or "WIP". Use `feat: add user login` or `fix: resolve memory leak`.
*   **Missing "How to Test"**: Forcing the reviewer to guess how to verify your changes delays the merge. Always provide repro steps.
*   **Ignoring "Draft" Status**: If the PR is not ready for review, mark it as "Draft" in your version control system (e.g., GitHub/GitLab) so reviewers don't waste time on incomplete work.