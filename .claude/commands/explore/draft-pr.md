---
description: Strategic Technical Consultation - Generate PR documentation
argument-hint: [exploration folder path] [optional: PR number]
---

# Issue to Pull Request Documentation

## Your Task

Generate a **comprehensive PR description** that bridges the exploration/design phase with the actual implementation on the current branch.

## Context

**You are invoked from the PR branch** - analyze the current branch's changes against the base branch.

## Input Requirements

1. **Exploration artifacts** (folder path in `$ARGUMENTS`):
   - `1-topic.md` - Original problem context
   - `2-report.md` - Technical exploration and decisions
   - `3-issue.md` - Implementation requirements

2. **Optional PR number** (if PR already exists):
   - Use to fetch PR metadata and comments
   - Otherwise, prepare for new PR creation

## Process

### Step 1: Analyze Exploration Context

1. Read all exploration files in the provided folder
2. Extract:
   - Original problem and requirements
   - Key design decisions and trade-offs
   - Planned implementation approach
   - Success criteria and risks

### Step 2: Examine Current Branch Implementation

**CRITICAL:** You're already on the PR branch - analyze changes from here.

```bash
# Analyze current branch changes
git diff $(git merge-base HEAD main)..HEAD --stat
git log $(git merge-base HEAD main)..HEAD --oneline

# If PR number provided, get additional context
gh pr view [PR_NUMBER] --json reviews,comments,checks

# Get list of changed files with details
git diff --name-status $(git merge-base HEAD main)..HEAD
```

**Code Analysis:**

- Identify main components changed
- Map implementation to planned design
- Note any deviations from plan
- Assess test coverage added

### Step 3: Generate PR Documentation

**CRITICAL:** Use the existing `4-pr.md` template in the exploration folder.

**Template Location:**

- Check for `4-pr.md` in the same directory as the exploration files
- If not present, copy from `docs/claude/explorations/_template/4-pr.md`

**Fill the template with:**

1. **Summary** - Connect to issue and exploration
2. **Changes** - What was actually implemented
3. **Implementation Notes** - Key decisions and deviations
4. **Testing** - Comprehensive validation approach
5. **Risk Assessment** - Updated risks from implementation
6. **Deployment** - Migration and breaking change details

## Analysis Framework

### Implementation Mapping

Compare planned vs actual implementation:

| Aspect     | From Issue      | As Implemented         | Reason for Change                   |
| ---------- | --------------- | ---------------------- | ----------------------------------- |
| Data Model | JSON column     | JSONB with GIN index   | Better query performance discovered |
| API Design | Simple endpoint | Paginated with filters | UX requirement emerged              |
| Caching    | Redis           | In-memory              | Simplified for MVP                  |

### Code Quality Assessment

Review implementation for:

- **Architecture adherence** - Follows codebase patterns?
- **Design alignment** - Matches exploration decisions?
- **Test coverage** - Maps to success criteria?
- **Performance** - Meets stated requirements?
- **Security** - Addresses identified risks?

### Documentation Requirements

The PR must clearly document:

1. **Connection** - Links to issue and exploration artifacts
2. **Changes** - Specific files and components modified
3. **Rationale** - Why implementation choices were made
4. **Validation** - How success criteria are met
5. **Impact** - Breaking changes, migrations, performance

## Quality Checklist

Before finalizing `4-pr.md`:

- [ ] Links to issue and exploration docs
- [ ] All changes documented with rationale
- [ ] Deviations from plan explained
- [ ] Test coverage maps to success criteria
- [ ] Migration/deployment notes included
- [ ] Performance impact assessed
- [ ] Breaking changes highlighted

## Example Transformation

**From Issue:**

> Implement PostgreSQL JSON column migration for 3x performance

**From Code Review:**

```python
# Added: app/models/property.py
class Property(Base):
    data = Column(JSONB)  # Changed from JSON to JSONB
    __table_args__ = (
        Index('idx_property_data', 'data', postgresql_using='gin'),
    )

# Added: migrations/002_json_migration.py
# Added: tests/test_property_performance.py (5 tests)
```

**To PR Description:**

> **Core Changes:**
>
> - **Property Model**: Migrated from EAV to JSONB with GIN indexing
>   - Files: `app/models/property.py`, `migrations/002_json_migration.py`
>   - Rationale: JSONB with GIN provides 3.5x query improvement (better than expected 3x)
>
> **Deviation:** Used JSONB instead of JSON as originally planned for better indexing support.

## Anti-Patterns to Avoid

### DON'T:

- Write generic PR descriptions
- Ignore deviations from plan
- Skip linking to exploration docs
- Copy issue text without implementation context
- Omit test validation details
- Forget migration/deployment impacts

### DO:

- Connect design to implementation
- Explain all technical choices
- Document what reviewers should focus on
- Provide clear validation steps
- Link all related documents
- Highlight risks and mitigations

## File Organization

```
exploration-folder/
├── 1-topic.md        # Problem definition
├── 2-report.md       # Exploration findings
├── 3-issue.md        # Requirements
├── 4-pr.md           # PR documentation (you create/update)
└── 5-retro.md        # Post-implementation learnings (optional)
```

## Success Metrics

A good PR description enables reviewers to:

- Understand the problem without reading all exploration docs
- See how implementation matches design intent
- Know what to test and validate
- Assess risks and impacts
- Make informed approval decisions
