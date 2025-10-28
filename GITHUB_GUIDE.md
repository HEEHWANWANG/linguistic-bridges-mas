# GitHub Integration Quick Start Guide

## 🎯 Overview

Version 3.0 adds complete Git and GitHub integration, allowing automatic version control for all code changes, experiment tracking, and collaborative development.

## 🚀 Quick Setup

### Step 1: Get GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "Linguistic Bridges MAS"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### Step 2: Configure .env

Add to your `.env` file:

```properties
# GitHub Configuration
GITHUB_TOKEN=ghp_YOUR_TOKEN_HERE
GITHUB_USERNAME=HEEHWANWANG
GITHUB_DEFAULT_REPO=HEEHWANWANG/linguistic-bridges
GIT_USER_NAME=HEEHWANWANG
GIT_USER_EMAIL=dhkdgmlghks@snu.ac.kr

# Git Behavior (optional - these are defaults)
GIT_AUTO_COMMIT=true
GIT_AUTO_PUSH=false
GIT_BRANCH_PREFIX=linguistic-bridges
GIT_COMMIT_MESSAGE_TEMPLATE=[{agent}] {action}: {description}
```

### Step 3: Initialize Repository

```bash
# Option 1: New repository (system will create .git)
python main.py

# Option 2: Existing repository
cd your-existing-repo
python /path/to/linguistic-bridges-mas/main.py

# Option 3: Manual initialization
git init
git remote add origin https://github.com/HEEHWANWANG/linguistic-bridges.git
python main.py
```

## 📋 What Gets Committed Automatically

### ✅ Automatic Commits (GIT_AUTO_COMMIT=true)

1. **Track Implementations**
   ```
   [TrackCoder] implemented: Track 1 - disentangled_representation_learning
   [TrackCoder] implemented: Track 2 - mediator_function_learning
   [TrackCoder] implemented: Track 3 - blueprint_driven_generation
   ```

2. **Data Pipeline Setup**
   ```
   [DataPipeline] added: ArtEmis and SDD dataset loaders
   ```

3. **Evaluation Results**
   ```
   [Evaluator] added: evaluation metrics and results
   ```

### ⚠️ Manual Approval Required (GIT_AUTO_PUSH=false)

Pushes to GitHub require human approval:
```
🔔 HUMAN APPROVAL REQUIRED
Agent: VersionControlAgent
Decision: Push changes to origin/main
Context: {
  "remote": "origin",
  "branch": "main"
}
Approve? (y/n):
```

## 🌿 Branch Management

### Experiment Branches

Each major experiment gets its own branch:
```python
# Automatic naming: {prefix}/{experiment}-{timestamp}
linguistic-bridges/track1-ablation-20251028-120530
linguistic-bridges/track2-optimization-20251028-143022
linguistic-bridges/full-pipeline-20251029-091545
```

### Branch Strategy

**Recommended workflow:**

1. **Main branch**: Stable, working versions
2. **Experiment branches**: One per research experiment
3. **Feature branches**: For specific improvements

```bash
main
├── linguistic-bridges/track1-ablation-20251028-120530
├── linguistic-bridges/track2-optimization-20251028-143022
└── linguistic-bridges/full-pipeline-20251029-091545
```

## 🔧 Configuration Options

### GIT_AUTO_COMMIT

- `true` (default): Automatically commit after each Track implementation
- `false`: Prompt for approval before each commit

**When to use `false`:**
- You want to review changes before committing
- Working on sensitive code
- Debugging and making frequent changes

### GIT_AUTO_PUSH

- `true`: Automatically push after commits (requires approval)
- `false` (default): Never push automatically

**When to use `true`:**
- Collaborative development
- Continuous integration setup
- Remote backup desired

### GIT_BRANCH_PREFIX

Customize your branch naming:
```properties
# Examples:
GIT_BRANCH_PREFIX=research        # research/experiment-name
GIT_BRANCH_PREFIX=exp             # exp/experiment-name
GIT_BRANCH_PREFIX=mas             # mas/experiment-name
```

### GIT_COMMIT_MESSAGE_TEMPLATE

Customize commit messages:
```properties
# Default:
GIT_COMMIT_MESSAGE_TEMPLATE=[{agent}] {action}: {description}

# Other options:
GIT_COMMIT_MESSAGE_TEMPLATE={action} ({agent}): {description}
GIT_COMMIT_MESSAGE_TEMPLATE=[MAS] {agent} - {action}: {description}
GIT_COMMIT_MESSAGE_TEMPLATE=🤖 {agent} | {action} | {description}
```

## 📊 Monitoring Version Control

### Check Repository Status

```bash
python cli.py status
```

Shows Git status along with system status.

### View Commit History

The system stores all commits in shared memory:
```python
# Retrieve from Vector DB
commits = await memory.query(
    query="recent commits",
    collection="version_control"
)
```

### Manual Git Operations

You can always use Git commands directly:
```bash
git status
git log --oneline
git branch -a
git diff
```

## 🔐 Security Best Practices

### 1. Protect Your Token
```bash
# ✅ Good: Token in .env (gitignored)
GITHUB_TOKEN=ghp_xxx

# ❌ Bad: Token in code
github_token = "ghp_xxx"
```

### 2. Use Fine-Grained Tokens

Instead of classic tokens, consider fine-grained tokens:
- Repo-specific access only
- Shorter expiration
- More granular permissions

### 3. Rotate Tokens Regularly

Change your GitHub token every 3-6 months.

### 4. Review Commits Before Pushing

With `GIT_AUTO_PUSH=false`, you control what goes to GitHub:
```bash
# Review before approving push
git log --oneline -5
git diff origin/main
```

## 🧪 Testing Without GitHub

Don't want to use GitHub? No problem:

```properties
# Leave blank to use local Git only
GITHUB_TOKEN=
GITHUB_USERNAME=
GITHUB_DEFAULT_REPO=

# Still get automatic commits locally
GIT_AUTO_COMMIT=true
GIT_AUTO_PUSH=false
```

System will:
- ✅ Initialize local Git repository
- ✅ Commit changes automatically
- ✅ Create branches
- ❌ Skip GitHub pushes

## 📝 Example Workflow

### Full Research Cycle

1. **System starts** → Git initialized
2. **Research Guild** generates hypotheses → Stored in Vector DB
3. **Forge Guild implements Track 1**:
   ```
   [TrackCoder] implemented: Track 1 - Disentanglement
   ```
   ✅ Automatically committed

4. **Track 1 succeeds** → Continue to Track 2
5. **Track 2 implemented**:
   ```
   [TrackCoder] implemented: Track 2 - Mediator Function
   ```
   ✅ Automatically committed

6. **All tracks complete** → Evaluation runs
7. **Results ready**:
   ```
   [Evaluator] added: Final evaluation results and plots
   ```
   ✅ Automatically committed

8. **Push to GitHub**:
   ```
   Approve? (y/n): y
   ```
   ✅ Pushed to GitHub

### Result
Complete project history on GitHub with meaningful commits!

## 🆘 Troubleshooting

### "Git not found"
```bash
# Install Git
# macOS:
brew install git

# Ubuntu/Debian:
sudo apt-get install git

# Windows:
# Download from https://git-scm.com/
```

### "Authentication failed"
- Check `GITHUB_TOKEN` is correct
- Token must have `repo` scope
- Token must not be expired

### "Nothing to commit"
- This is normal if no files changed
- System only commits when there are changes

### "Push rejected"
- Pull latest changes first:
  ```bash
  git pull origin main
  ```
- Resolve any conflicts
- Try push again

## 💡 Pro Tips

1. **Commit Messages**: Use descriptive experiment names for better history
2. **Branch Cleanup**: Periodically delete old experiment branches
3. **Backup**: GitHub serves as automatic backup for your code
4. **Collaboration**: Share experiment branches with team members
5. **CI/CD**: GitHub integration enables automated testing

## 📚 Further Reading

- [Git Documentation](https://git-scm.com/doc)
- [GitHub API](https://docs.github.com/en/rest)
- [Git Best Practices](https://git-scm.com/book/en/v2)

---

**Version**: 3.0  
**Updated**: October 28, 2025  
**Related**: See `CHANGELOG.md` for version history
