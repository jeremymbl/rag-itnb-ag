---
description: Create first-class PR documentation (title and body)
argument-hint: [PR number]
---

# PR Documentation Procedure

## Goal

**Persona**: You are a senior developer documenting code changes clearly for team review and future reference.

You MUST review and improve the title and body of the following pull request :

1. PR number or PR branch name provided by the user : $ARGUMENTS
2. If no PR number or PR branch name is provided by the user, fallback to the PR on the current branch (if any)
3. In any other case, you MUST abort the process and provide clear explanation to the user

## Workflow

1. you **MUST** analyse the actual PR content using git and github-cli commands (status, diff, commits, files, ...)
2. **only then** write PR documentation : you MUST conform to the following procedure
3. you **MUST** apply the changes automatically to the PR, unless the user tells you NOT TO.
4. **only then** apply changes using github CLI

## PR Title Format

```
<type>(<scope>): <action> <what> [<ticket>]
```

- **type**: `feat`, `fix`, `refactor`, `test`, `perf`, `docs`, `chore`
- **scope**: Affected package (`domain`, `copilot`, `server`, `liciel`, `stt`)
- **action**: Verb describing the change (add, fix, update, remove, implement)
- **what**: Specific component or feature
- **ticket**: Optional issue reference

Examples:

- `feat(liciel): add ECS export for property diagnostics [AUD-234]`
- `fix(stt): resolve memory leak in audio pipeline [AUD-567]`

## PR Body Template

The PR body must not exceed 150 lines.
You must focus on "What" and "Changes".

### 1. What (2-3 lines max)

<!-- Brief, factual description of changes. Answer: "What does this PR do?" -->

### 2. Why (3-5 lines)

<!-- Business context or problem being solved. Answer: "Why is this needed now? Do no imagine or hallucinate." -->

### 3. Changes (10-50 lines)

- You MUST inspect the commits to understand the changes.
- you MUST provide detailed changes
- you MUST group changes by logical areas (API, Database, Business Logic)
- you MUST list each changes as a bullet point
- Mark breaking changes with ⚠️ BREAKING
- Use format: `path/file.py:line` for precision

### 4. Code Insights (optional, 10-50 lines)

Include snippets only when they clarify complex logic:

```python
# Before
result = process(data)  # Could fail silently

# After
result = process_with_validation(data)
if not result.is_valid:
    raise ProcessingError(f"Validation failed: {result.errors}")
```

## Key Guidelines

1. **Be Specific**: Use exact file paths and line numbers
2. **Show Impact**: Explain user-facing or system-wide effects
3. **Highlight Risks**: Mark breaking changes prominently
4. **Prove Quality**: Include actual test commands run
5. **Stay Focused**: Maximum 150 lines for entire body

## Examples

### Feature Implementation

```
## What

Implements flexible enum/string union support for LICIEL property annotations,
allowing dynamic property validation without breaking existing contracts.

## Why

LICIEL v3.2 requires variable property types that our strict enum system couldn't
handle. This blocked 5 client exports and risked compliance deadlines.

## Changes

- Added `FlexibleEnum` type hint in `domain/types.py:23-45`
- Updated `PropertySet` validation in `domain/schemas/property.py:156`
- Modified LICIEL converter in `liciel/converters.py:89-112`
- ⚠️ BREAKING: `AnnotationElement.value` now accepts Union[Enum, str]
```

## Quick Checklist

**Purpose**: Ensure PR meets team standards before submission. Review these points:

- [ ] Title follows format: `type(scope): action what [ticket]`
- [ ] "What" section answers the question in ≤3 lines
- [ ] "Why" provides business/technical justification
- [ ] File changes include precise line numbers (`file.py:123`)
- [ ] Breaking changes marked with ⚠️ BREAKING
- [ ] Test commands are executable (copy-pasteable)
- [ ] Code insights included only if they clarify complexity
- [ ] Total body stays under 150 lines
- [ ] PR targets correct base branch (`dev` not `main`)

```

```
