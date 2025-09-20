# Branch Protection Rules

This document outlines the branch protection rules and workflow for the MLOps project.

## Branch Structure

### 1. `dev` Branch
- **Purpose**: Development work and feature implementation
- **Protection Rules**:
  - Require pull request reviews (1 reviewer minimum)
  - Require status checks to pass before merging
  - Require branches to be up to date before merging
  - Restrict pushes to the branch (only via pull requests)

### 2. `test` Branch
- **Purpose**: Testing and validation of features
- **Protection Rules**:
  - Require pull request reviews (1 reviewer minimum)
  - Require status checks to pass before merging
  - Require branches to be up to date before merging
  - Restrict pushes to the branch (only via pull requests)

### 3. `master` Branch
- **Purpose**: Production-ready code
- **Protection Rules**:
  - Require pull request reviews (2 reviewers minimum)
  - Require status checks to pass before merging
  - Require branches to be up to date before merging
  - Restrict pushes to the branch (only via pull requests)
  - Include administrators in protection rules

## Admin Approval Workflow

### Group Admin Responsibilities
1. **Review and Approve Pull Requests**
   - Code quality review
   - Functionality testing
   - Documentation review
   - Security considerations

2. **Merge Approvals**
   - `dev` → `test`: Requires admin approval
   - `test` → `master`: Requires admin approval

3. **Emergency Procedures**
   - Hotfix procedures for critical issues
   - Rollback procedures if needed

### Pull Request Process
1. Developer creates feature branch from `dev`
2. Developer implements feature and creates PR to `dev`
3. Admin reviews and approves PR to `dev`
4. Feature is merged to `dev`
5. Admin creates PR from `dev` to `test`
6. Automated testing runs on `test` branch
7. Admin reviews test results and creates PR to `master`
8. Automated deployment runs on `master` branch

## Required Status Checks

### For `dev` Branch
- [ ] Code quality check (flake8)
- [ ] Security scan (bandit)
- [ ] Basic unit tests

### For `test` Branch
- [ ] All `dev` checks
- [ ] Comprehensive unit tests
- [ ] Integration tests
- [ ] Performance tests

### For `master` Branch
- [ ] All `test` checks
- [ ] Docker build test
- [ ] Deployment readiness check

## Notification System

### Email Notifications
- **Success**: Admin receives email on successful deployment
- **Failure**: Admin receives email on deployment failure
- **PR Updates**: Admin receives notifications for PR status changes

### Slack Integration (Optional)
- Deployment status updates
- Build failure notifications
- PR approval requests

## Emergency Procedures

### Hotfix Process
1. Create hotfix branch from `master`
2. Implement fix and create PR to `master`
3. Admin reviews and approves
4. Deploy immediately to production
5. Backport fix to `dev` and `test` branches

### Rollback Process
1. Identify problematic commit
2. Create rollback PR
3. Admin approves rollback
4. Deploy previous stable version
5. Investigate and fix issues in `dev` branch

