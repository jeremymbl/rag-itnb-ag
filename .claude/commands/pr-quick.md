---
description: Full workflow to prepare a PR from current changes
---

# Quick PR Preparation Procedure

## Goal

**Persona**: You are a senior developer documenting code changes clearly for team review and future reference.

This procedure tells you how to prepare a first class PR from a bunch of changes.
You **MUST** follow the precise workflow bellow.

## Workflow

1. If no changes are staged, you MUST stage all changes first
2. If current branch is `dev` or `main` you must create a dedicated tmp branch **locally** for the PR to commit the staged changes (use this format `pr-tmp-YYYYMMDDTHHMM`)
3. Commit the staged changes to the **local** branch : you **MUST** follow exaclty the procedure in @.claude/commands/commit.md. **DON'T** request user approval : just do it.
4. When all plan commits are done, prepare the PR. you MUST follow these steps in the specified order :
   1. follow exactly the procedure in @.claude/commands/pr-document.md.
   2. rename the local tmp branch name to better reflect the intent of the PR (Prefix it with the assignees initials (example : "ldp-my-branch-name" for "Lionel du Peloux", "ac-my-branch-name" for "Aurélien Cabiac", ...))
   3. publish the local branch to the remote
   4. create the PR according to the preparation you've made at point 4.1 : DO NOT ask for user approval, dot it.
   5. assign the PR to my self

### Example

```bash
# 1. If current branch is main/dev, create a temporary branch
git checkout -b pr-tmp-$(date -u +"%Y%m%dT%H%M")

# 2. Stage and commit changes (see @.claude/commands/commit.md)
git add .
git commit -m "Your commit message here"

# Repeat commits as needed...

# 3. Document the PR (see @.claude/commands/pr-document.md)

# 4. Rename tmp branch to meaningful name, prefixed by your initials
git branch -m pr-tmp-20250911T1315 ldp-offline-sync-fix

# 5. Publish branch to remote
git push -u origin ldp-offline-sync-fix

# 6. Create PR (draft if still WIP, otherwise standard)
gh pr create --fill --assignee @me

# The PR now exists, assigned to you, with correct branch name and prepared doc
```
