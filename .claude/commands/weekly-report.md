---
description: Generate code activity weekly report
argument-hint: [week num or date - current week if blank]
---

# Weekly Activity Report Generation Procedure

## Personae

**Report Audience**: Development team leads, project managers, and stakeholders requiring visibility into weekly code progress and technical decisions.

## Objectives

- Provide comprehensive overview of development velocity and code changes
- Highlight technical achievements and key implementation decisions
- Track pull request activity and code quality metrics
- Enable data-driven sprint planning and resource allocation

## Generation Process

### Report Periode

User-specified **week number** or **date** : $ARGUMENTS

**YOU MUST** determine for which week the user wants to establish the report :

- If the user has specified a **week number** (`WW`) : you must compute the monday/sunday dates for this week for the **current** year and generate the report for this week

- If the user has specified a **date** (`DD/MM/YYYY`) : you must find the week number for this date, and then fallback to point `1.`

- If the user has specified nothing : you must find the current week number for today, and then fallback to point `1.`

**YOU MUST** ask user confirmation about the selected week before you continue the procedure.

### Data Collection

- Query GitHub API for specified repositories (see bellow)
- For each repository, get the list of the merged/closed PR for the report periode
- For each PR in the list collect relevant data to established the report
- Extract detailed commit information including author, lines added/removed per commit
- Calculate contributor code line ratios based on individual commit statistics (not PR merge author)
- Aggregate commit statistics and file changes per contributor
- Calculate per-contributor code line ratios across all PRs based on actual commit contributions
- report PR count per repo in the tile (example : "### `frontend-app` (x3)")

### Repositories

**YOU MUST BUILD THE REPORT FOR THIS EXACT LIST OF REPOSITORIES:**

- `mvp-diag-assist-back`
- `mvp-diag-assist-front`

### Report Assembly

- Generate markdown sections per template structure
- Calculate summary metrics across all repositories
- Format technical highlights by domain/topic

### Output Generation

- Output folder : @docs/reports/
- Output file : YYYY#WW - weekly activity report.md
- **YOU MUST** conform to the template provided bellow

#### Report template structure (to follow)

```markdown
# Weekly Code Activity Report (#10-2024)

**Week**: March 4-10, 2024 (Week 10)
**Generated**: March 11, 2024

## Global Summary

**Total Activity**: 12 pull requests merged | +2,847 / -1,203 lines of code | 67 commits

**Contributors**: Alice Johnson (5 PRs, 65% lines), Bob Smith (4 PRs, 25% lines), Charlie Brown (3 PRs, 10% lines)

Key achievements this week focused on authentication system refactoring and performance optimizations across frontend and backend components.

## Technical Highlights

### Authentication & Security

- Implemented OAuth 2.0 integration with multi-provider support
- Enhanced JWT token validation and refresh mechanisms
- Added rate limiting middleware for API endpoints

### Performance Optimization

- Database query optimization reducing response times by 40%
- Frontend bundle size reduction through code splitting
- Implemented Redis caching layer for frequently accessed data

### Infrastructure

- Migrated CI/CD pipeline to GitHub Actions
- Added automated security scanning in deployment process

## Pull Requests by Repository

### `frontend-app` (x3)

#### [#142](https://github.com/owner/frontend-app/pull/142) - Implement OAuth login component

**Impact**: Enables users to authenticate via Google, GitHub, and Microsoft accounts, reducing registration friction and improving user onboarding experience.

**Code Changes**:

- Added OAuth provider configuration and callback handlers
- Implemented secure token storage in HTTP-only cookies
- Created reusable authentication context provider
- Updated login/signup UI components with provider buttons
- Added error handling for OAuth flow failures
- Integrated with backend authentication endpoints

**Contributors**: Alice Johnson (70% lines), Bob Smith (30% lines)
**Metrics**: +456 / -23 lines | 8 files | 12 commits | 2 contributors
**Key Files**: `src/auth/OAuthProvider.tsx`, `src/components/LoginForm.tsx`, `src/hooks/useAuth.ts`

#### [#143](https://github.com/owner/frontend-app/pull/143) - Bundle optimization and code splitting

**Impact**: Reduces initial bundle size by 35%, improving page load times and user experience, particularly on mobile devices and slower connections.

**Code Changes**:

- Implemented route-based code splitting with React.lazy
- Configured Webpack bundle analyzer and optimization settings
- Added preload hints for critical resources
- Optimized asset imports and removed unused dependencies
- Implemented progressive loading for dashboard components

**Contributors**: Alice Johnson (100% lines)
**Metrics**: +189 / -67 lines | 15 files | 8 commits | 1 contributor
**Key Files**: `webpack.config.js`, `src/pages/Dashboard.tsx`, `src/utils/lazyLoad.ts`

### `backend-api` (x2)

#### [#89](https://github.com/owner/backend-api/pull/89) - Database query optimization

**Impact**: Improves API response times by 40% through optimized database queries, enhanced indexing strategy, and reduced N+1 query problems.

**Code Changes**:

- Added composite indexes for frequently queried columns
- Implemented query result caching with Redis
- Optimized ORM relations and eager loading strategies
- Added database query performance monitoring
- Refactored complex queries to use raw SQL where beneficial
- Updated API pagination to use cursor-based approach

**Contributors**: Bob Smith (50% lines), Charlie Brown (30% lines), David Wilson (20% lines)
**Metrics**: +234 / -156 lines | 12 files | 18 commits | 3 contributors
**Key Files**: `src/models/User.js`, `src/controllers/dashboard.js`, `migrations/add_composite_indexes.sql`
```
