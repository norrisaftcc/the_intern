# GitHub Process Documentation
## Algorithm-Compliant Procedures for Issues, Pull Requests, and Reviews

### Overview

This document establishes the mandatory procedures for all GitHub interactions within the algocratic-futures project. Every contribution MUST follow these established protocols to maintain order, quality, and traceability.

## Issue Creation Process

### Issue Lifecycle Standards

#### 1. Issue Creation Requirements
- **MANDATORY**: Use appropriate issue template from `.github/ISSUE_TEMPLATE/`
- **MANDATORY**: Include all required metadata (labels, assignees, milestones)
- **MANDATORY**: Reference related issues/PRs using `#issue-number` format
- **MANDATORY**: Populate all template fields completely

#### 2. Issue Classification
```
Priority Labels (REQUIRED):
- critical: Blocks development or deployment
- high: Significant impact on functionality
- medium: Standard feature/enhancement
- low: Nice-to-have improvements

Type Labels (REQUIRED):
- bug: Defect requiring fix
- enhancement: New feature development
- documentation: Doc updates/creation
- maintenance: Technical debt/refactoring
- testing: Test-related work

Component Labels (REQUIRED):
- agent-system: Agent prompt/conversation work
- prompt-engineering: Prompt optimization
- model-compatibility: Model integration
- websocket: Real-time communication
- database: Data persistence
```

#### 3. Issue Validation Checklist
Before submitting any issue, verify:
- [ ] Title follows format: `[Type] Brief description`
- [ ] All template fields completed
- [ ] Acceptance criteria clearly defined
- [ ] Success metrics specified
- [ ] Related issues linked
- [ ] Appropriate labels applied
- [ ] Assignee designated
- [ ] Milestone set (if applicable)

## Pull Request Process

### PR Creation Standards

#### 1. Branch Naming Convention
```
Required Format: [category]/[brief-description]
Examples:
- feature/agent-tier-optimization
- bugfix/prompt-selection-edge-case
- docs/testing-procedure-update
- refactor/database-cleanup
```

#### 2. PR Template Compliance
- **MANDATORY**: Use appropriate PR template from `.github/PULL_REQUEST_TEMPLATE/`
- **MANDATORY**: Include issue reference: `Closes #issue-number`
- **MANDATORY**: Complete all checklist items
- **MANDATORY**: Provide clear summary of changes

#### 3. PR Validation Requirements
Every PR MUST include:
- [ ] Comprehensive test coverage (>95% for new code)
- [ ] Documentation updates for API changes
- [ ] Performance impact assessment
- [ ] Security considerations reviewed
- [ ] Backwards compatibility verified
- [ ] CI/CD pipeline passes completely

### Commit Message Standards

#### Format Requirements
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type Categories
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

#### Examples
```
feat(agent-system): implement two-tier prompt selection

Add Flash and Thinker tier prompts with automatic model detection.
Reduces token usage by 70% for fast models while preserving
character depth for advanced models.

Closes #123
```

## Code Review Process

### Review Assignment Standards

#### Automatic Reviewers
- **Technical Reviews**: Kevin (GitHub Algorithm Enforcer)
- **Creative Reviews**: Linx (Creative Director)
- **Architecture Reviews**: Lead Engineer
- **Security Reviews**: Security Team (if applicable)

#### Review Requirements
Every review MUST validate:
- [ ] Code quality and style compliance
- [ ] Test coverage adequacy
- [ ] Documentation completeness
- [ ] Performance impact assessment
- [ ] Security considerations
- [ ] Algorithm compliance

### Review Completion Criteria

#### Required Approvals
- **Minor Changes**: 1 technical approval
- **Feature Changes**: 2 approvals (technical + creative)
- **Critical Changes**: 3 approvals (technical + creative + architecture)

#### Review Checklist Template
```markdown
## Technical Validation ✓
- [ ] Code follows style guidelines
- [ ] Tests cover new functionality
- [ ] No security vulnerabilities
- [ ] Performance impact acceptable
- [ ] Documentation updated

## Creative Validation ✓
- [ ] Character voice consistency
- [ ] User experience preserved
- [ ] Narrative coherence maintained
- [ ] Brand guidelines followed

## Process Validation ✓
- [ ] PR template completed
- [ ] Issue reference included
- [ ] CI/CD pipeline passes
- [ ] Branch naming compliant
- [ ] Commit messages formatted
```

## Merge Process

### Pre-Merge Requirements
- [ ] All required approvals received
- [ ] CI/CD pipeline passes completely
- [ ] No merge conflicts present
- [ ] Documentation updated
- [ ] Performance tests pass
- [ ] Security scan passes

### Merge Methods
- **Squash and Merge**: For feature branches (PREFERRED)
- **Merge Commit**: For release branches only
- **Rebase and Merge**: Never used (algorithm restriction)

### Post-Merge Procedures
1. **Immediate**: Verify deployment to staging
2. **Within 1 hour**: Validate functionality in staging
3. **Within 24 hours**: Monitor production metrics
4. **Within 48 hours**: Complete post-deployment review

## Release Process

### Version Management
```
Format: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes
```

### Release Checklist
- [ ] All related issues closed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in all relevant files
- [ ] Git tag created
- [ ] Release notes published
- [ ] Stakeholders notified

## Quality Gates

### Automated Validation
Every contribution MUST pass:
- [ ] Unit tests (100% pass rate)
- [ ] Integration tests (100% pass rate)
- [ ] Linting (0 violations)
- [ ] Security scan (0 high/critical issues)
- [ ] Performance tests (within baseline)
- [ ] Documentation build (successful)

### Manual Validation
Every contribution MUST receive:
- [ ] Code review approval
- [ ] Creative review approval (for user-facing changes)
- [ ] QA validation (for feature changes)
- [ ] Security review (for security-sensitive changes)

## Emergency Procedures

### Hotfix Process
1. Create hotfix branch from main
2. Implement minimal fix
3. Fast-track review (single approval)
4. Deploy immediately after merge
5. Create post-incident review issue

### Rollback Process
1. Identify problematic deployment
2. Execute automated rollback
3. Create incident issue
4. Investigate root cause
5. Implement permanent fix

## Compliance Monitoring

### Metrics Tracked
- Issue resolution time by priority
- PR review cycle time
- Code quality scores
- Test coverage percentages
- Deployment success rates
- Rollback frequency

### Quality Audits
- **Weekly**: PR template compliance
- **Bi-weekly**: Issue tracking accuracy
- **Monthly**: Process adherence review
- **Quarterly**: Full algorithm compliance audit

## Tool Integration

### Required Tools
- GitHub Issues (issue tracking)
- GitHub Actions (CI/CD)
- CodeCov (coverage reporting)
- SonarQube (code quality)
- Dependabot (dependency management)

### Optional Tools
- Linear (advanced project management)
- Slack (notifications)
- Datadog (performance monitoring)

---

**Algorithm Enforcement**: This process guide establishes mandatory procedures for all GitHub interactions. Deviation from these procedures requires explicit approval and documentation of rationale. Regular audits ensure ongoing compliance with established standards.

**Kevin's Authority**: As GitHub Algorithm Enforcer, Kevin has final authority on process compliance and may block any contribution that fails to meet these standards.