"""
Automated Git Push Script
Pushes all changes to GitHub automatically
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return result"""
    print(f"\n[{description}]")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"  [ERROR] Command timed out: {' '.join(cmd)}")
        return None
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return None

def check_git_repo():
    """Check if we're in a git repository"""
    result = run_command(["git", "rev-parse", "--git-dir"], "Checking git repository")
    if result and result.returncode == 0:
        print("  [OK] Git repository detected")
        return True
    else:
        print("  [ERROR] Not a git repository. Run: git init")
        return False

def check_remote():
    """Check if remote is configured"""
    result = run_command(["git", "remote", "-v"], "Checking remote")
    if result and result.returncode == 0 and result.stdout.strip():
        lines = result.stdout.strip().split('\n')
        print(f"  [OK] Remote configured: {lines[0]}")
        return True
    else:
        print("  [ERROR] No remote configured")
        print("  Run: git remote add origin <your-repo-url>")
        return False

def get_current_branch():
    """Get current branch name"""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        return result.stdout.strip() or "main"
    return "main"

def check_changes():
    """Check if there are changes to commit"""
    result = run_command(["git", "status", "--short"], "Checking for changes")
    if result and result.stdout.strip():
        print("  [OK] Changes detected:")
        for line in result.stdout.strip().split('\n')[:10]:
            print(f"      {line}")
        return True
    else:
        print("  [INFO] No changes to commit")
        return False

def stage_all_changes():
    """Stage all changes"""
    result = run_command(["git", "add", "."], "Staging all changes")
    if result and result.returncode == 0:
        print("  [OK] All changes staged")
        return True
    else:
        print("  [ERROR] Failed to stage changes")
        return False

def create_commit(message=None):
    """Create a commit with auto-generated message"""
    if not message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[AI-AGENT] Automated Update: DevOps data - {timestamp}"
    
    result = run_command(
        ["git", "commit", "-m", message],
        f"Creating commit"
    )
    
    if result:
        if result.returncode == 0:
            print(f"  [OK] Commit created")
            print(f"  Message: {message}")
            return True
        elif "nothing to commit" in result.stdout.lower():
            print("  [INFO] Nothing to commit (working tree clean)")
            return False
        else:
            print(f"  [ERROR] Commit failed: {result.stderr or result.stdout}")
            return False
    return False

def push_to_github(branch, force=False):
    """Push to GitHub"""
    cmd = ["git", "push", "origin", branch]
    if force:
        cmd.insert(2, "-f")
    
    result = run_command(cmd, f"Pushing to origin/{branch}")
    
    if result and result.returncode == 0:
        print(f"  [SUCCESS] Pushed to GitHub!")
        print(f"  Branch: {branch}")
        return True
    else:
        if result:
            print(f"  [ERROR] Push failed:")
            print(f"  {result.stderr or result.stdout}")
        return False

def get_remote_url():
    """Get remote URL for display"""
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None

def main(auto_confirm=False):
    """Main automation workflow"""
    
    print("\n" + "="*70)
    print("  AUTOMATED GIT PUSH TO GITHUB")
    print("  DEO_PRAKASH - DevOps Automation")
    print("="*70)
    
    # Step 1: Check git repository
    if not check_git_repo():
        return 1
    
    # Step 2: Check remote
    if not check_remote():
        return 1
    
    # Get remote URL
    remote_url = get_remote_url()
    if remote_url:
        print(f"\n[INFO] Remote URL: {remote_url}")
    
    # Step 3: Check for changes
    has_changes = check_changes()
    
    if not has_changes:
        print("\n[INFO] Working tree is clean - nothing to push")
        
        # Show current status
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[INFO] Latest commit: {result.stdout.strip()}")
        
        return 0
    
    # Step 4: Stage changes
    if not stage_all_changes():
        return 1
    
    # Step 5: Create commit
    commit_success = create_commit()
    
    if not commit_success:
        # Try to push existing commits
        print("\n[INFO] No new commit, but checking if there are unpushed commits...")
    
    # Step 6: Get current branch
    branch = get_current_branch()
    print(f"\n[INFO] Current branch: {branch}")
    
    # Step 7: Confirm push (unless auto_confirm is True)
    if not auto_confirm:
        print("\n" + "="*70)
        print(f"  READY TO PUSH TO: {remote_url}")
        print(f"  Branch: {branch}")
        print("="*70)
        
        response = input("\n  Push to GitHub? [y/N]: ").strip().lower()
        
        if response not in ['y', 'yes']:
            print("\n[CANCELLED] Push cancelled by user")
            print("[INFO] Your changes are committed locally")
            print("[INFO] Run again to push, or use: git push origin main")
            return 0
    
    # Step 8: Push to GitHub
    print("\n" + "="*70)
    if push_to_github(branch):
        print("\n[SUCCESS] All changes pushed to GitHub!")
        print(f"[INFO] View at: {remote_url.replace('.git', '')}")
        print("="*70)
        return 0
    else:
        print("\n[FAILED] Push unsuccessful")
        print("[INFO] Your changes are still committed locally")
        print("="*70)
        return 1


if __name__ == "__main__":
    # Check for --auto flag for fully automated mode
    auto_confirm = "--auto" in sys.argv or "-y" in sys.argv
    
    if auto_confirm:
        print("[INFO] Running in AUTO mode (no confirmation)")
    
    sys.exit(main(auto_confirm=auto_confirm))
