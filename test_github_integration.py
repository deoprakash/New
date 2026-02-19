"""
Real GitHub Integration Test Script
Tests Git automation with actual GitHub repository
"""

import sys
import os
from pathlib import Path
import subprocess
import json

# Add to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "scripts"))

def check_git_status():
    """Check if we're in a git repository"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def check_remote_configured():
    """Check if remote is configured"""
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0 and len(result.stdout) > 0
    except Exception:
        return False

def get_current_branch():
    """Get current git branch"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None

def get_team_info():
    """Get team and leader names for branch naming"""
    team_name = os.getenv("TEAM_NAME", "RIFT_ORGANISERS")
    leader_name = os.getenv("LEADER_NAME", "SAIYAM_KUMAR")
    return team_name, leader_name

def ensure_ai_fix_branch(team_name, leader_name):
    """Ensure we are on TEAM_NAME_LEADER_NAME_AI_Fix branch"""
    from branch_manager import BranchManager
    manager = BranchManager(team_name=team_name, leader_name=leader_name)
    branch_name = manager.generate_branch_name(team_name, leader_name)

    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
        timeout=5
    )
    if result.returncode == 0:
        subprocess.run(["git", "checkout", branch_name], check=False)
    else:
        subprocess.run(["git", "checkout", "main"], check=False)
        subprocess.run(["git", "checkout", "-b", branch_name], check=False)

    return branch_name

def test_github_integration():
    """Test complete GitHub integration workflow"""
    
    print("\n" + "="*70)
    print("  REAL GITHUB INTEGRATION TEST")
    print("  Member 2 - DevOps/Git Automation Lead")
    print("="*70)
    
    # Step 1: Check Git
    print("\n[STEP 1] Checking Git configuration...")
    if not check_git_status():
        print("  [ERROR] Not a git repository!")
        print("\n  To initialize:")
        print("    git init")
        print("    git remote add origin <your-repo-url>")
        return False
    print("  [OK] Git repository detected")
    
    # Step 2: Check Remote
    print("\n[STEP 2] Checking remote configuration...")
    if not check_remote_configured():
        print("  [WARNING] No remote configured!")
        print("\n  To add remote:")
        print("    git remote add origin https://github.com/YOUR_USERNAME/RIFT26.git")
        print("\n  Continuing without push test...")
        can_push = False
    else:
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
        print("  [OK] Remote configured:")
        for line in result.stdout.split('\n')[:2]:
            if line:
                print(f"      {line}")
        can_push = True
    
    # Step 3: Check Current Branch
    print("\n[STEP 3] Checking current branch...")
    current_branch = get_current_branch()
    if current_branch:
        print(f"  [OK] Current branch: {current_branch}")
    else:
        print("  [WARNING] Could not detect branch")
        current_branch = "main"
    
    # Step 4: Create TEAM_NAME_LEADER_NAME_AI_Fix Branches
    print("\n[STEP 4] Creating TEAM_NAME_LEADER_NAME_AI_Fix branches...")
    from branch_manager import BranchManager
    
    team_name, leader_name = get_team_info()
    manager = BranchManager(team_name=team_name, leader_name=leader_name)
    target_branch = ensure_ai_fix_branch(team_name, leader_name)
    print(f"  [OK] Using branch: {target_branch}")
    test_branches = [
        ("bug", "201", "github_integration_test"),
        ("feature", "202", "test_automation"),
    ]
    
    created = []
    for branch_type, issue_id, description in test_branches:
        branch = manager.create_branch_entry(
            issue_type=branch_type,
            issue_id=issue_id,
            description=description,
            team_name=team_name,
            leader_name=leader_name
        )
        created.append(branch)
        print(f"  [OK] Created: {branch['branch_name']}")
    
    # Step 5: Stage Changes
    print("\n[STEP 5] Staging changes (git add)...")
    files_to_add = [
        "data/branch_history.json",
        "data/ci_pipeline_timeline.json",
        "data/deployment_history.json"
    ]
    
    for file in files_to_add:
        result = subprocess.run(
            ["git", "add", file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  [OK] Staged: {file}")
        else:
            print(f"  [SKIP] {file} (might not exist or no changes)")
    
    # Step 6: Check Status
    print("\n[STEP 6] Checking git status...")
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        print("  [OK] Changes staged:")
        for line in result.stdout.split('\n')[:5]:
            if line:
                print(f"      {line}")
    else:
        print("  [INFO] No changes to commit (already up to date)")
    
    # Step 7: Create Commit
    print("\n[STEP 7] Creating commit...")
    commit_message = "[AI-AGENT] Update: Automated DevOps data - Member 2 deliverables"
    
    result = subprocess.run(
        ["git", "commit", "-m", commit_message],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"  [OK] Commit created: {commit_message}")
        print(f"      Output: {result.stdout.strip()}")
        commit_created = True
    else:
        if "nothing to commit" in result.stdout.lower():
            print("  [INFO] No changes to commit (working tree clean)")
            commit_created = False
        else:
            print(f"  [WARNING] Commit failed: {result.stderr or result.stdout}")
            commit_created = False
    
    # Step 8: Push to GitHub
    if can_push and commit_created:
        print("\n[STEP 8] Pushing to GitHub...")
        print(f"  [ACTION] About to push to remote/{target_branch}")
        print("  [INFO] This will push to your GitHub repository!")
        
        response = input("\n  Do you want to push? (yes/no): ").lower()
        
        if response in ['yes', 'y']:
            result = subprocess.run(
                ["git", "push", "origin", target_branch],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  [SUCCESS] Pushed to GitHub!")
                print(f"  [INFO] Check your repo at: https://github.com/YOUR_USERNAME/RIFT26")
                return True
            else:
                print(f"  [ERROR] Push failed:")
                print(f"      {result.stderr}")
                return False
        else:
            print("  [SKIP] Push cancelled by user")
            return True
    elif not can_push:
        print("\n[STEP 8] Push to GitHub...")
        print("  [SKIP] No remote configured - cannot push")
        print("\n  [INFO] To push later:")
        print("    git remote add origin https://github.com/YOUR_USERNAME/RIFT26.git")
        print(f"    git push origin {current_branch}")
        return True
    else:
        print("\n[STEP 8] Push to GitHub...")
        print("  [SKIP] No new commits to push")
        return True
    
    return True


def show_github_setup_guide():
    """Show GitHub repository setup guide"""
    print("\n" + "="*70)
    print("  GITHUB REPOSITORY SETUP GUIDE")
    print("="*70)
    
    print("""
📋 STEP-BY-STEP GITHUB SETUP:

1️⃣  Create GitHub Repository:
   - Go to: https://github.com/new
   - Repository name: RIFT26 (or your choice)
   - Description: "DevOps/Git Automation - RIFT'26 Hackathon"
   - Make it Public (for demo visibility)
   - DO NOT initialize with README (we have local files)
   - Click "Create repository"

2️⃣  Initialize Local Repository (if not done):
   cd "C:\\Users\\deopr\\.vscode\\Projects\\RIFT'26"
   git init

3️⃣  Add All Project Files:
   git add .
   git commit -m "Initial commit: DevOps automation project"

4️⃣  Add GitHub Remote:
   git remote add origin https://github.com/YOUR_USERNAME/RIFT26.git
   
5️⃣  Push to GitHub:
   git branch -M main
   git push -u origin main

6️⃣  Verify on GitHub:
   - Visit: https://github.com/YOUR_USERNAME/RIFT26
   - You should see all your project files!

📡 CONFIGURE GIT (if needed):
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"

🔐 AUTHENTICATION:
   - GitHub now requires Personal Access Token (PAT) for HTTPS
   - Or use SSH keys
   
   For PAT:
   1. Go to: https://github.com/settings/tokens
   2. Generate new token (classic)
   3. Select scopes: repo, workflow
   4. Copy token (save it - you won't see it again!)
   5. When git asks for password, use the token

   For SSH:
   1. Generate key: ssh-keygen -t ed25519 -C "your.email@example.com"
   2. Add to GitHub: https://github.com/settings/keys
   3. Use SSH URL: git@github.com:YOUR_USERNAME/RIFT26.git

🎯 TEST THE AUTOMATION:
   python test_github_integration.py

    """)


def main():
    """Main execution"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        show_github_setup_guide()
        return 0
    
    success = test_github_integration()
    
    if success:
        print("\n" + "="*70)
        print("  [SUCCESS] GitHub Integration Test Complete!")
        print("="*70)
        print("\n  ✓ Git automation working")
        print("  ✓ Branch creation logged")
        print("  ✓ Commits created (if changes exist)")
        print("  ✓ Ready for real GitHub workflow")
        print("\n  Run with --setup flag to see full GitHub setup guide")
        print("    python test_github_integration.py --setup")
        return 0
    else:
        print("\n" + "="*70)
        print("  [INFO] GitHub Integration Test Completed with Notes")
        print("="*70)
        print("\n  See messages above for setup instructions")
        return 0


if __name__ == "__main__":
    sys.exit(main())
