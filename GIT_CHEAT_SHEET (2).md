# Git & GitHub Cheat Sheet

A comprehensive guide for Git and GitHub operations - from initial setup to advanced workflows.

---

## Table of Contents

1. [Initial Project Setup](#1-initial-project-setup)
2. [Daily Safe Workflow](#2-daily-safe-workflow)
3. [Branch Operations](#3-branch-operations)
4. [Making Changes](#4-making-changes)
5. [Pull Requests](#5-pull-requests)
6. [Merging & Conflicts](#6-merging--conflicts)
7. [Undoing Changes](#7-undoing-changes)
8. [Repository Management](#8-repository-management)
9. [Quick Reference](#9-quick-reference)
10. [Troubleshooting](#10-troubleshooting)
11. [Best Practices](#11-best-practices)
12. [ADW Workflows](#12-adw-workflows)

---

## 1. Initial Project Setup

### First Time: Push a New Project to GitHub

```bash
# 1. Initialize Git repository
git init

# 2. Add remote repository
git remote add origin https://github.com/username/repository.git

# 3. Check what files you have
git status

# 4. Stage all files
git add .

# 5. Create initial commit
git commit -m "Initial commit: project setup"

# 6. Push to GitHub (first time)
git push -u origin main
# OR if using master:
git push -u origin master

# 7. Verify remote
git remote -v
```

### Clone Existing Repository

```bash
# Clone repository
git clone https://github.com/username/repository.git

# Navigate into project
cd repository

# Check status
git status
```

---

## 2. Daily Safe Workflow

**Golden Rule:** Never commit directly to `main`! Always use feature branches.

### Complete Safe Workflow

```bash
# Step 1: Start from updated main
git checkout main
git pull origin main

# Step 2: Create feature branch
git checkout -b feature/my-new-feature

# Step 3: Make your changes
# ... edit files ...

# Step 4: Check what changed
git status
git diff

# Step 5: Stage changes
git add .
# OR stage specific files:
git add src/App.tsx src/styles.css

# Step 6: Commit with descriptive message
git commit -m "feat: add user profile page"

# Step 7: Push feature branch to GitHub
git push origin feature/my-new-feature

# Step 8: Create Pull Request (on GitHub or via CLI)
gh pr create --title "Add user profile" --body "Description here"

# Step 9: After PR is approved and merged on GitHub
git checkout main
git pull origin main

# Step 10: Delete feature branch
git branch -d feature/my-new-feature
git push origin --delete feature/my-new-feature
```

---

## 3. Branch Operations

### Creating Branches

```bash
# Create new branch
git branch feature/new-feature

# Create and switch to new branch
git checkout -b feature/new-feature

# Create branch from specific commit
git checkout -b hotfix/bug abc1234
```

### Switching Branches

```bash
# Switch to existing branch
git checkout main
git checkout feature/my-feature

# Switch to previous branch
git checkout -
```

### Viewing Branches

```bash
# List local branches
git branch

# List all branches (local + remote)
git branch -a

# List remote branches only
git branch -r

# Show branch with last commit
git branch -v
```

### Deleting Branches

```bash
# Delete local branch (safe - warns if unmerged)
git branch -d feature/old-feature

# Force delete local branch
git branch -D feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

### Renaming Branches

```bash
# Rename current branch
git branch -m new-name

# Rename specific branch
git branch -m old-name new-name

# Rename master to main
git branch -m master main
git push -u origin main
git push origin --delete master
```

---

## 4. Making Changes

### Staging Changes

```bash
# Stage all changes
git add .

# Stage specific file
git add src/App.tsx

# Stage specific directory
git add src/components/

# Stage all JavaScript files
git add *.js

# Stage parts of a file (interactive)
git add -p
```

### Committing Changes

```bash
# Commit with message
git commit -m "fix: resolve login bug"

# Commit with detailed message
git commit -m "feat: add dark mode

- Added toggle in header
- Saved preference to localStorage
- Updated all components for dark mode"

# Commit all tracked changes (skip git add)
git commit -am "chore: update dependencies"

# Amend last commit (change message or add files)
git add forgotten-file.txt
git commit --amend
```

### Commit Message Conventions

```bash
# Feature
git commit -m "feat: add user authentication"

# Bug fix
git commit -m "fix: resolve date formatting issue"

# Documentation
git commit -m "docs: update API documentation"

# Code refactoring
git commit -m "refactor: simplify user service logic"

# Tests
git commit -m "test: add unit tests for auth module"

# Chores (maintenance)
git commit -m "chore: update npm dependencies"

# Performance improvement
git commit -m "perf: optimize database queries"

# Style changes
git commit -m "style: format code with prettier"
```

### Pushing Changes

```bash
# Push to remote branch
git push origin feature/my-feature

# Push with upstream tracking (first time)
git push -u origin feature/my-feature

# After upstream is set, simply:
git push

# Push all branches
git push origin --all

# Force push (DANGEROUS - use with caution!)
git push -f origin feature/my-feature
```

---

## 5. Pull Requests

### Creating Pull Requests

**Via GitHub CLI:**
```bash
# Create PR with title and body
gh pr create --title "Add user profile" --body "Implements user profile page with edit functionality"

# Create PR interactively
gh pr create

# Create draft PR
gh pr create --draft
```

**Via GitHub Website:**
1. Push your feature branch
2. Go to repository on GitHub
3. Click "Compare & pull request" button
4. Fill in title and description
5. Click "Create pull request"

### Managing Pull Requests

```bash
# List all PRs
gh pr list

# View specific PR
gh pr view 123

# Check out PR locally
gh pr checkout 123

# Merge PR
gh pr merge 123

# Close PR without merging
gh pr close 123

# Reopen closed PR
gh pr reopen 123
```

---

## 6. Merging & Conflicts

### Merging Branches

```bash
# Merge feature into current branch
git checkout main
git merge feature/my-feature

# Merge with no fast-forward (creates merge commit)
git merge --no-ff feature/my-feature

# Merge unrelated histories (when branches don't share history)
git merge feature/my-feature --allow-unrelated-histories
```

### Handling Merge Conflicts

When you see:
```
Auto-merging src/App.tsx
CONFLICT (content): Merge conflict in src/App.tsx
Automatic merge failed; fix conflicts and then commit the result.
```

**Resolution steps:**

```bash
# 1. Check which files have conflicts
git status

# 2. Open conflicted files and look for:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> feature/my-feature

# 3. Edit the file to resolve conflicts

# 4. Stage resolved files
git add src/App.tsx

# 5. Complete the merge
git commit -m "Merge feature/my-feature into main"

# OR abort the merge
git merge --abort
```

### Conflict Resolution Strategies

```bash
# Keep your version (current branch)
git checkout --ours conflicted-file.txt
git add conflicted-file.txt

# Keep their version (merging branch)
git checkout --theirs conflicted-file.txt
git add conflicted-file.txt
```

### Rebasing (Advanced)

```bash
# Rebase current branch onto main
git checkout feature/my-feature
git rebase main

# Interactive rebase (edit history)
git rebase -i HEAD~3

# Abort rebase
git rebase --abort

# Continue after resolving conflicts
git rebase --continue
```

---

## 7. Undoing Changes

### Before Staging (Working Directory)

```bash
# Discard all changes
git restore .

# Discard changes in specific file
git restore src/App.tsx

# Discard changes in directory
git restore src/components/
```

### After Staging (Staged Changes)

```bash
# Unstage all files
git restore --staged .

# Unstage specific file
git restore --staged src/App.tsx
```

### After Committing (Local Only)

```bash
# Undo last commit, keep changes
git reset HEAD~1

# Undo last 3 commits, keep changes
git reset HEAD~3

# Undo last commit, discard changes (DANGEROUS!)
git reset --hard HEAD~1

# Undo to specific commit
git reset abc1234
git reset --hard abc1234
```

### After Pushing (Public History)

```bash
# Create new commit that undoes changes (SAFE)
git revert HEAD
git revert abc1234

# Revert multiple commits
git revert HEAD~3..HEAD

# Force push to overwrite (DANGEROUS - avoid on main!)
git reset --hard abc1234
git push -f origin feature/my-feature
```

### Recovering Lost Commits

```bash
# View all actions (including deleted commits)
git reflog

# Restore to previous state
git reset --hard HEAD@{2}

# Create branch from lost commit
git branch recovered-branch abc1234
```

---

## 8. Repository Management

### Remote Operations

```bash
# View remotes
git remote -v

# Add remote
git remote add origin https://github.com/user/repo.git

# Change remote URL
git remote set-url origin https://github.com/user/new-repo.git

# Remove remote
git remote remove origin

# Rename remote
git remote rename origin upstream

# Fetch from remote (doesn't merge)
git fetch origin

# Pull from remote (fetch + merge)
git pull origin main

# Pull with rebase
git pull --rebase origin main
```

### Repository Information

```bash
# View commit history
git log

# Compact history
git log --oneline

# Last 5 commits
git log --oneline -5

# Visual branch history
git log --graph --oneline --all

# Show changes in commit
git show abc1234

# View file history
git log -- src/App.tsx

# Search commits
git log --grep="bug fix"
git log --author="John"
```

### Viewing Changes

```bash
# View unstaged changes
git diff

# View staged changes
git diff --staged

# Compare branches
git diff main..feature/my-feature

# Compare with remote
git diff main origin/main

# View file at specific commit
git show abc1234:src/App.tsx
```

### Tags

```bash
# Create tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# List tags
git tag

# Push tag to remote
git push origin v1.0.0

# Push all tags
git push origin --tags

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

### GitHub Branch Protection

**On GitHub Website:**
1. Go to: `https://github.com/username/repo/settings/branches`
2. Click "Add branch protection rule"
3. Branch name pattern: `main`
4. Enable:
   - ☑️ Require pull request before merging
   - ☑️ Require status checks to pass
   - ☑️ Require conversation resolution before merging
   - ☑️ Do not allow bypassing settings
5. Click "Create"

**Effect:**
- Cannot push directly to main
- Must use pull requests
- Enforces code review

---

## 9. Quick Reference

### Essential Commands Table

| Operation | Command |
|-----------|---------|
| **Initialize repo** | `git init` |
| **Clone repo** | `git clone <url>` |
| **Check status** | `git status` |
| **Stage all** | `git add .` |
| **Stage file** | `git add <file>` |
| **Commit** | `git commit -m "message"` |
| **Push** | `git push origin <branch>` |
| **Pull** | `git pull origin <branch>` |
| **Create branch** | `git checkout -b <branch>` |
| **Switch branch** | `git checkout <branch>` |
| **Merge branch** | `git merge <branch>` |
| **Delete local branch** | `git branch -d <branch>` |
| **Delete remote branch** | `git push origin --delete <branch>` |
| **View branches** | `git branch -a` |
| **View log** | `git log --oneline` |
| **Discard changes** | `git restore <file>` |
| **Undo commit** | `git reset HEAD~1` |
| **Revert commit** | `git revert HEAD` |

### Branch Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| **Feature** | `feature/<description>` | `feature/user-auth` |
| **Bug fix** | `fix/<description>` | `fix/login-error` |
| **Hotfix** | `hotfix/<description>` | `hotfix/critical-bug` |
| **Chore** | `chore/<description>` | `chore/update-deps` |
| **Refactor** | `refactor/<description>` | `refactor/api-cleanup` |

---

## 10. Troubleshooting

### Common Errors & Solutions

#### Error: "fatal: refusing to merge unrelated histories"

**Problem:** Branches don't share common history

**Solution:**
```bash
git merge <branch> --allow-unrelated-histories
```

---

#### Error: "error: failed to push some refs"

**Problem:** Remote has changes you don't have locally

**Solution:**
```bash
# Pull first, then push
git pull origin main
git push origin main

# OR rebase
git pull --rebase origin main
git push origin main
```

---

#### Error: "error: Your local changes would be overwritten"

**Problem:** You have uncommitted changes

**Solution:**
```bash
# Option 1: Commit changes
git add .
git commit -m "WIP: work in progress"

# Option 2: Stash changes
git stash
git pull origin main
git stash pop

# Option 3: Discard changes
git restore .
```

---

#### Error: "fatal: not a git repository"

**Problem:** Not in a Git repository

**Solution:**
```bash
# Initialize repository
git init

# OR navigate to repository
cd /path/to/repository
```

---

#### Error: "fatal: remote origin already exists"

**Problem:** Remote already configured

**Solution:**
```bash
# View existing remote
git remote -v

# Update remote URL
git remote set-url origin <new-url>

# OR remove and re-add
git remote remove origin
git remote add origin <url>
```

---

#### Pushed to Wrong Branch

**Problem:** Committed and pushed to main instead of feature branch

**Solution:**
```bash
# Create branch from current state
git branch feature/my-work

# Reset main to match remote
git checkout main
git reset --hard origin/main

# Switch to feature branch
git checkout feature/my-work
```

---

#### Need to Split a Commit

**Problem:** One commit contains multiple unrelated changes

**Solution:**
```bash
# Interactive rebase
git rebase -i HEAD~1

# Change 'pick' to 'edit' for the commit
# Then:
git reset HEAD~1
git add <file1>
git commit -m "First change"
git add <file2>
git commit -m "Second change"
git rebase --continue
```

---

## 11. Best Practices

### ✅ DO

- **Always work on feature branches**
- **Write clear, descriptive commit messages**
- **Commit often with logical chunks**
- **Pull before pushing**
- **Review changes before committing** (`git diff`)
- **Use `.gitignore` for generated files**
- **Protect main branch with branch protection rules**
- **Create pull requests for code review**
- **Delete branches after merging**
- **Keep commits atomic** (one logical change per commit)

### ❌ DON'T

- **Never commit directly to main**
- **Don't commit secrets** (API keys, passwords)
- **Don't commit large binary files**
- **Don't use `git push -f` on shared branches**
- **Don't commit commented-out code** (use git history instead)
- **Don't commit unfinished work to main**
- **Don't make commits with message "fix" or "update"**
- **Don't rewrite public history** (commits already pushed)

### Commit Message Guidelines

**Good:**
```bash
git commit -m "feat: add user authentication with OAuth

- Implement OAuth2 login flow
- Add JWT token management
- Create user session handling
- Add tests for auth module"
```

**Bad:**
```bash
git commit -m "update"
git commit -m "fix stuff"
git commit -m "changes"
```

### File Organization

**Always `.gitignore`:**
```gitignore
# Dependencies
node_modules/
venv/
.venv/

# Environment variables
.env
.env.local

# Build outputs
dist/
build/
*.pyc
__pycache__/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

---

## 12. ADW Workflows

### How ADW Uses Git

The ADW (AI Developer Workflow) system follows Git best practices automatically:

#### ADW Workflow Phases

```bash
# Run complete ADW pipeline
cd adws
uv run adw_plan_build_test_review.py <issue-number>
```

**What ADW does automatically:**

1. **Planning Phase** (`adw_plan.py`):
   ```bash
   # ADW creates feature branch
   git checkout -b feat-123-abc1234-add-user-profile

   # ADW commits plan
   git add specs/123_abc1234_plan_spec.md
   git commit -m "plan: add user profile feature"
   git push origin feat-123-abc1234-add-user-profile
   ```

2. **Build Phase** (`adw_build.py`):
   ```bash
   # ADW implements code
   git add src/ app/
   git commit -m "feat: implement user profile page"
   git push origin feat-123-abc1234-add-user-profile
   ```

3. **Test Phase** (`adw_test.py`):
   ```bash
   # ADW runs tests and fixes issues
   git add tests/ src/
   git commit -m "test: fix failing tests"
   git push origin feat-123-abc1234-add-user-profile
   ```

4. **Review Phase** (`adw_review.py`):
   ```bash
   # ADW reviews and creates patches
   git add .
   git commit -m "fix: resolve review issues"
   git push origin feat-123-abc1234-add-user-profile
   ```

5. **Pull Request**:
   - ADW creates PR automatically
   - PR targets `main` branch
   - Includes screenshots and documentation

### ADW Branch Naming

ADW creates branches following this pattern:
```
<type>-<issue-number>-<adw-id>-<description>
```

Examples:
- `feat-123-abc1234-add-dark-mode`
- `fix-456-def5678-resolve-login-bug`
- `chore-789-ghi9012-update-dependencies`

### Manual ADW Operations

```bash
# Run individual phases
cd adws

# Planning only
uv run adw_plan.py 123

# Build only (requires existing plan)
uv run adw_build.py 123 abc1234

# Test only
uv run adw_test.py 123 abc1234

# Review only
uv run adw_review.py 123 abc1234
```

### ADW State Management

ADW tracks workflow state in:
```
agents/<adw-id>/adw_state.json
```

Contains:
- `adw_id` - Unique workflow identifier
- `issue_number` - GitHub issue number
- `branch_name` - Feature branch name
- `plan_file` - Path to implementation plan
- `issue_class` - Issue type (`/feature`, `/bug`, `/chore`)

### Interacting with ADW Branches

```bash
# Check out ADW branch
git checkout feat-123-abc1234-add-user-profile

# View ADW changes
git log --oneline

# Make manual changes on ADW branch
git add .
git commit -m "manual: adjust styling"
git push origin feat-123-abc1234-add-user-profile

# Merge ADW PR manually
git checkout main
git merge feat-123-abc1234-add-user-profile
git push origin main
git branch -d feat-123-abc1234-add-user-profile
```

---

## Appendix: Configuration

### Git Global Configuration

```bash
# Set user name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default editor
git config --global core.editor "code --wait"

# Set default branch name
git config --global init.defaultBranch main

# Enable color output
git config --global color.ui auto

# View all configuration
git config --list

# View specific setting
git config user.name
```

### Useful Git Aliases

```bash
# Add aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --graph --oneline --all"

# Use aliases
git st    # Instead of git status
git co main    # Instead of git checkout main
git br -a    # Instead of git branch -a
git lg    # Beautiful log graph
```

---

## Quick Start Checklist

### Starting a New Project

- [ ] `git init`
- [ ] `git remote add origin <url>`
- [ ] `git add .`
- [ ] `git commit -m "Initial commit"`
- [ ] `git push -u origin main`

### Daily Development

- [ ] `git checkout main`
- [ ] `git pull origin main`
- [ ] `git checkout -b feature/my-feature`
- [ ] Make changes
- [ ] `git add .`
- [ ] `git commit -m "feat: description"`
- [ ] `git push origin feature/my-feature`
- [ ] Create pull request
- [ ] Merge PR on GitHub
- [ ] `git checkout main && git pull`
- [ ] `git branch -d feature/my-feature`

---

**Last Updated:** 2025-01-11

**Repository:** [TAC-5-6](https://github.com/NithishTU/TAC-5-6)

**Related Documentation:**
- [README.md](./README.md) - Project overview
- [adws/README.md](./adws/README.md) - ADW system documentation
- [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md) - Getting started guide
