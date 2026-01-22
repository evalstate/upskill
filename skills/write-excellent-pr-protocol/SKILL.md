---
name: write-excellent-pr-protocol
description: Guide an AI to craft clear, thorough pull requests for standardized protocol changes
---

# Writing an Excellent Pull Request for a Standardized Protocol

## Overview  
Pull requests (PRs) that modify a protocol specification must be precise, reproducible, and easy for reviewers to assess. This guide outlines the structure, content, and common checks to ensure a PR communicates *what* changed, *why* it changed, and *how* it has been validated against the protocol’s standards.

## Step‑by‑Step Instructions  

1. **Title** – Use a concise, conventional format:  
   ```
   <type>(<module>): <short description>
   ```  
   *type*: `feat`, `fix`, `doc`, `refactor`, `test`.  
   *module*: part of the protocol (e.g., `handshake`, `frame`, `error-codes`).  

2. **Summary (Header)** – One‑paragraph overview answering:  
   - What part of the spec is affected?  
   - Why is the change needed (bug, new feature, clarification)?  

3. **Detailed Description** – Include the following sections, each labelled with a heading:  
   - **Background** – Link to the existing spec section, issue tracker, or external proposal.  
   - **Change Summary** – Bullet list of modifications (e.g., “Add `0x1A` error code”, “Rename `CONNECT` to `INIT`”).  
   - **Rationale** – Explain design decisions, compatibility impact, and any deprecation plan.  
   - **Specification Diff** – Embed a markdown table or code block comparing old vs. new wording.  

4. **Implementation Evidence** – Provide concrete artifacts:  
   ```yaml
   # Example: Updated protocol definition fragment
   messages:
     - name: INIT
       id: 0x01
       fields:
         - { name: version, type: uint8 }
   ```  

5. **Testing & Validation** – List test suites run, sample packet captures, or conformance tool output. Include commands:  
   ```bash
   $ protocheck --spec new_spec.yaml --tests test_suite/
   ```  

6. **Documentation Updates** – Reference any README, changelog, or user‑guide sections updated.  

7. **Checklist** – Tick required items before merging:  
   - [ ] Title follows convention  
   - [ ] All affected spec sections updated  
   - [ ] Tests pass (`npm test`, `pytest`, etc.)  
   - [ ] Reviewer tags added  

## Example PR Skeleton  

```markdown
feat(handshake): add optional TLS negotiation flag

### Summary
Introduce `tls_negotiation` flag to the initial handshake allowing clients to
opt‑in to TLS without a separate negotiation round.

### Background
Current spec §2.1 requires a separate `TLS_START` message. This change aligns
with RFC 8446 recommendations.

### Change Summary
- New boolean field `tls_negotiation` in `Handshake` message.
- Updated state diagram to show optional TLS path.
- Deprecated `TLS_START` message (will be removed in v2.0).

### Specification Diff
```diff
- message Handshake {
-   uint8 version;
- }
+ message Handshake {
+   uint8 version;
+   bool tls_negotiation = optional;
+ }
```

### Testing
```bash
protocheck --spec spec/v1.3.yaml --tests tests/handshake/
```

All existing tests pass; new test `test_tls_flag.py` validates optional path.

### Checklist
- [x] Title follows convention
- [x] Spec updated
- [x] Tests added and passing
- [x] Documentation links updated
```

## Best Practices & Pitfalls  

- **Never merge without a diff view** – reviewers need a clear before/after.  
- **Maintain backward compatibility** – explicitly state version bumps or deprecation schedules.  
- **Avoid vague language** – use precise terminology from the spec glossary.  
- **Provide reproducible test commands** – reviewers should be able to run them locally.  
- **Limit scope** – a PR should address one logical change; split large updates into multiple PRs.