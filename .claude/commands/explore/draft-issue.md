---
description: Strategic Technical Consultation - Transform exploration & review reports into actionable GitHub issue
argument-hint: [exploration folder path]
---

# Report to GitHub Issue Transformation

## Your Task

Transform the technical exploration report into a **concise, actionable GitHub issue** ready for copy-paste to GitHub.

## Process

### Step 1: Locate Files

1. Read the topic and report files provided in the folder : `$ARGUMENTS`
2. Check for existing `3-issue.md` in same directory or fallback to the template in `@claude/explorations/_template/`

### Step 2: Use Template

**CRITICAL:** The `3-issue.md` template already exists in the same directory as the report.

- **DO NOT** create the file from scratch
- **USE** the existing `3-issue.md` template file
- **FILL IN** all placeholder sections with content from the report

### Step 3: Transform Content

Using the existing `3-issue.md` template, fill in each section:

1. **Extract from Report:**
   - Problem statement from exploration context
   - Chosen solution from final recommendation
   - Key decisions from decision log
   - Requirements from requirements section
   - Risks from risk assessment

2. **Synthesize for Issue:**
   - Condense exploration journal into key design decisions
   - Convert implementation roadmap into concrete task lists
   - Transform success metrics into measurable criteria
   - Simplify technical specification into implementation plan

## Transformation Guidelines

### DO:

- **Use the existing template** - It's already in the directory
- **Be concise** - GitHub issues should be scannable
- **Be specific** - Use concrete examples from report
- **Be actionable** - Every task should be implementable
- **Preserve decisions** - Include key trade-offs with brief rationale
- **Link documents** - Reference report and topic files

### DON'T:

- Create a new file structure - use the template
- Include exploration journey details
- Copy entire sections verbatim
- Add implementation code
- Include rejected alternatives (unless critical)
- Exceed 2 pages in length

## Quality Checklist

Before finalizing:

- [ ] Used existing `3-issue.md` template
- [ ] Title clearly states what will be done
- [ ] Problem is understandable standalone
- [ ] Solution is concrete and implementable
- [ ] Tasks are specific and assignable
- [ ] Success criteria are measurable
- [ ] Risks from exploration are captured
- [ ] Links to report and topic are included

## Example Transformation

**From Report (verbose):**

> After extensive analysis comparing multiple approaches including EAV models, JSONB columns, and separate tables, we determined that PostgreSQL's native JSON columns provide the optimal balance of performance and flexibility. Testing showed 3x query speed improvement and 50% storage reduction compared to our current EAV implementation...

**To Issue (concise):**

> **Problem:** Current EAV model causes 300ms+ query latency for property searches.
>
> **Solution:** Migrate to PostgreSQL native JSON columns for 3x performance gain.
>
> **Key Decision**: JSON over EAV because [performance: 3x faster, storage: 50% less]

## File Organization

Standard exploration directory structure:

```
exploration-folder/
├── 1-topic.md        # Original problem definition (input)
├── 2-report.md       # Exploration findings (input)
├── 3-issue.md        # GitHub issue (you update this)
└── 4-pr.md           # PR template (for implementation)
```

**Remember:**

- If the templates are already there : use them!
- Otherwise, look into @claude/explorations/\_template/
