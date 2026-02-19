# Real GitHub Integration Guide
# Member 2 - DevOps/Git Automation Lead

## 🎯 Quick Start - Test with Real GitHub

### Step 1: Run the Integration Test
```bash
python test_github_integration.py
```

This will:
- ✅ Check if git is initialized
- ✅ Verify remote configuration
- ✅ Create TEAM_NAME_LEADER_NAME_AI_Fix branches
- ✅ Stage and commit changes
- ✅ Push to GitHub (with your confirmation)

### Step 2: View Full Setup Guide
```bash
python test_github_integration.py --setup
```

---

## 📋 Manual GitHub Setup (First Time)

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `RIFT26`
3. **Description:** `DevOps/Git Automation - RIFT'26 Hackathon - Member 2 Deliverables`
4. **Visibility:** Public (for judges to see)
5. **DO NOT** initialize with README (we have local files)
6. Click **Create repository**

### 2. Initialize Local Git

```bash
cd "c:\Users\deopr\.vscode\Projects\RIFT'26"

# Initialize git (if not already done)
git init

# Configure git user
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 3. Add All Files

```bash
# Add all project files
git add .

# Create initial commit
git commit -m "Initial commit: DevOps automation project - Member 2"
```

### 4. Connect to GitHub

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/RIFT26.git

# Verify remote
git remote -v
```

### 5. Push to GitHub

```bash
# Set main branch and push
git branch -M main
git push -u origin main
```

---

## 🔐 GitHub Authentication

### Option A: Personal Access Token (Recommended for HTTPS)

1. Go to https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. **Note:** "RIFT26 DevOps Automation"
4. **Expiration:** 30 days (for hackathon)
5. **Select scopes:**
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
6. Click **Generate token**
7. **COPY THE TOKEN** (you won't see it again!)
8. When git asks for password, paste the token

### Option B: SSH Keys (Alternative)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

Then:
1. Go to https://github.com/settings/keys
2. Click **New SSH key**
3. Paste your public key
4. Use SSH URL: `git@github.com:YOUR_USERNAME/RIFT26.git`

---

## 🚀 Test Real GitHub Workflow

### Test 1: Create and Push Branch

```bash
# Run the test script
python test_github_integration.py

# It will:
# 1. Create TEAM_NAME_LEADER_NAME_AI_Fix branches
# 2. Update data files
# 3. Commit changes
# 4. Ask if you want to push
```

### Test 2: Manual Git Workflow

```bash
# Create some changes
python scripts/branch_manager.py

# Check status
git status

# Stage changes
git add data/

# Commit with proper message format
git commit -m "[AI-AGENT] Update: Branch history - Member 2"

# Push to GitHub
git push origin main
```

### Test 3: Create Feature Branch

```bash
# Create a new branch for testing
git checkout -b feature/test-automation

# Make changes
python main.py

# Commit and push new branch
git add .
git commit -m "[AI-AGENT] Feature: Test automation workflow"
git push origin feature/test-automation
```

---

## 📊 Verify on GitHub

After pushing, check your repository at:
```
https://github.com/YOUR_USERNAME/RIFT26
```

You should see:
- ✅ All project files
- ✅ data/ folder with JSON files
- ✅ scripts/ folder with automation
- ✅ Commit history with [AI-AGENT] messages
- ✅ Branch history in data/branch_history.json

---

## 🎯 Demo for Hackathon Judges

### Show Live Git Automation:

```bash
# 1. Run full workflow
python main.py

# 2. Show generated data
cat data/branch_history.json
cat data/ci_pipeline_timeline.json

# 3. Commit and push
git add data/
git commit -m "[AI-AGENT] Demo: Automated CI/CD pipeline execution"
git push origin main

# 4. Show on GitHub
# Open browser: https://github.com/YOUR_USERNAME/RIFT26/commits
```

### Show TEAM_NAME_LEADER_NAME_AI_Fix Branches:

```bash
# View branch history
python -c "import json; print(json.dumps(json.load(open('data/branch_history.json')), indent=2))"
```

---

## 🔧 Troubleshooting

### Issue: "fatal: not a git repository"
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/RIFT26.git
```

### Issue: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/RIFT26.git
```

### Issue: "Authentication failed"
- Use Personal Access Token instead of password
- Or set up SSH keys

### Issue: "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

### Issue: "nothing to commit"
- Good! Means everything is already committed
- Run automation to generate new data

---

## 📝 Commit Message Format

Use this format for consistency (judges love this!):

```
[AI-AGENT] <Type>: <Description>

Types:
- Update: Data files updated
- Feature: New functionality
- Fix: Bug fix
- Demo: Demo-specific changes

Examples:
✅ [AI-AGENT] Update: Branch history generated
✅ [AI-AGENT] Feature: CI/CD pipeline automation
✅ [AI-AGENT] Fix: Docker configuration updated
✅ [AI-AGENT] Demo: Complete workflow execution
```

---

## 🎬 Full Demo Script

```bash
# 1. Initial Setup (one time)
git init
git remote add origin https://github.com/YOUR_USERNAME/RIFT26.git
git add .
git commit -m "[AI-AGENT] Initial: DevOps automation project"
git push -u origin main

# 2. Run Automation
python main.py

# 3. Test GitHub Integration
python test_github_integration.py

# 4. View Results on GitHub
# Open: https://github.com/YOUR_USERNAME/RIFT26

# 5. Show to Judges!
```

---

## ✅ Success Checklist

Before demo:
- [ ] GitHub repository created
- [ ] Remote configured (`git remote -v`)
- [ ] All files committed and pushed
- [ ] data/ folder visible on GitHub
- [ ] Commit messages follow format
- [ ] Branch history has entries
- [ ] CI/CD timeline has data
- [ ] Test script runs successfully

---

## 🚀 Ready for Hackathon!

Your GitHub integration is ready when:
1. ✅ Repository is public on GitHub
2. ✅ All automation code is pushed
3. ✅ Data files show real results
4. ✅ Commit history looks professional
5. ✅ You can run `python main.py` → commit → push → visible on GitHub

**Pro tip:** Record a quick video showing the automation → GitHub update flow!
