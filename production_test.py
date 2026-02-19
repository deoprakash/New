"""
Production-Ready GitHub Integration Test
Generates fresh data and tests complete workflow
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import random

# Add to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "scripts"))
sys.path.insert(0, str(project_root / "ci_cd" / "pipeline"))
sys.path.insert(0, str(project_root / "deployment"))


def print_step(step_num, title, status=""):
    """Print formatted step"""
    if status == "OK":
        print(f"\n[Step {step_num}] {title} ... [OK]")
    elif status == "FAIL":
        print(f"\n[Step {step_num}] {title} ... [FAIL]")
    elif status == "SKIP":
        print(f"\n[Step {step_num}] {title} ... [SKIP]")
    else:
        print(f"\n[Step {step_num}] {title}")


def clean_data_files():
    """Clean old data files for fresh test"""
    print_step(1, "Cleaning old data files")
    
    data_dir = project_root / "data"
    json_files = list(data_dir.glob("*.json"))
    
    if not json_files:
        print("No data files to clean")
        print_step(1, "Cleaning old data files", "SKIP")
        return
    
    for file in json_files:
        try:
            file.unlink()
            print(f"  Deleted: {file.name}")
        except Exception as e:
            print(f"  Error deleting {file.name}: {e}")
    
    print_step(1, "Cleaning old data files", "OK")


def generate_branch_data(count=8):
    """Generate production-quality branch data"""
    print_step(2, f"Generating {count} production branches")
    
    try:
        from branch_manager import BranchManager
        
        branch_mgr = BranchManager()
        branches = []
        
        # Enhanced branch scenarios for production demo
        scenarios = [
            ("bug", "101", "auth_token_expiration"),
            ("feature", "102", "user_dashboard_redesign"),
            ("hotfix", "103", "critical_memory_leak"),
            ("fix", "104", "api_response_timeout"),
            ("feature", "105", "multi_language_support"),
            ("bug", "106", "payment_validation_error"),
            ("hotfix", "107", "database_connection_pool"),
            ("feature", "108", "real_time_notifications"),
        ]
        
        for i, (branch_type, issue_id, description) in enumerate(scenarios[:count], 1):
            branch_data = branch_mgr.create_branch_entry(
                issue_type=branch_type,
                issue_id=issue_id,
                description=description
            )
            branches.append(branch_data)
            print(f"  [{i}/{count}] Created: {branch_data['type']} - {description}")
        
        print_step(2, f"Generating {count} production branches", "OK")
        return branches
        
    except Exception as e:
        print(f"Error: {e}")
        print_step(2, f"Generating {count} production branches", "FAIL")
        return []


def generate_ci_pipeline_data(iterations=5):
    """Generate production CI/CD timeline data"""
    print_step(3, f"Running {iterations} CI pipeline iterations")
    
    try:
        from ci_runner import CIRunner
        
        # Force simulation mode for production demo
        runner = CIRunner(use_simulation=True)
        
        print(f"  Running in SIMULATION mode (production-safe)")
        
        # Run multiple iterations with varying results
        results = []
        for i in range(iterations):
            print(f"  [{i+1}/{iterations}] Running iteration {i+1}...")
            result = runner.simulate_pipeline_run()
            results.append(result)
            
            # Brief pause between iterations
            if i < iterations - 1:
                import time
                time.sleep(0.5)
        
        # Save to timeline
        runner.save_pipeline_data()
        
        # Statistics
        passed = sum(1 for r in results if r['status'] == 'passed')
        failed = iterations - passed
        
        print(f"\n  Results: {passed} passed, {failed} failed")
        print_step(3, f"Running {iterations} CI pipeline iterations", "OK")
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print_step(3, f"Running {iterations} CI pipeline iterations", "FAIL")
        return []


def generate_deployment_data():
    """Generate deployment history"""
    print_step(4, "Simulating deployment operations")
    
    try:
        from deploy import DeploymentManager
        
        deploy_mgr = DeploymentManager()
        
        # Simulate Railway deployment
        print("  [1/2] Deploying to Railway...")
        railway_result = deploy_mgr.deploy_railway(service_name="rift26-backend")
        
        # Simulate AWS deployment
        print("  [2/2] Deploying to AWS Lambda...")
        aws_result = deploy_mgr.deploy_aws(
            region="us-east-1",
            service_type="lambda"
        )
        
        # Save deployment history
        deploy_mgr.save_deployment_history()
        
        print_step(4, "Simulating deployment operations", "OK")
        return [railway_result, aws_result]
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print_step(4, "Simulating deployment operations", "FAIL")
        return []


def verify_data_files():
    """Verify all data files were created correctly"""
    print_step(5, "Verifying generated data files")
    
    data_dir = project_root / "data"
    required_files = [
        "branch_history.json",
        "ci_pipeline_timeline.json",
        "deployment_history.json"
    ]
    
    all_valid = True
    
    for filename in required_files:
        filepath = data_dir / filename
        
        if not filepath.exists():
            print(f"  [MISSING] {filename}")
            all_valid = False
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if file has data
            if isinstance(data, list) and len(data) == 0:
                print(f"  [EMPTY] {filename}")
                all_valid = False
            elif isinstance(data, dict) and len(data.get('pipeline_history', [])) == 0:
                print(f"  [EMPTY] {filename}")
                all_valid = False
            else:
                size_kb = filepath.stat().st_size / 1024
                print(f"  [OK] {filename} ({size_kb:.1f} KB)")
        
        except json.JSONDecodeError:
            print(f"  [INVALID] {filename} - Invalid JSON")
            all_valid = False
        except Exception as e:
            print(f"  [ERROR] {filename} - {e}")
            all_valid = False
    
    if all_valid:
        print_step(5, "Verifying generated data files", "OK")
    else:
        print_step(5, "Verifying generated data files", "FAIL")
    
    return all_valid


def show_data_summary():
    """Show summary of generated data"""
    print("\n" + "="*60)
    print("DATA GENERATION SUMMARY")
    print("="*60)
    
    data_dir = project_root / "data"
    
    # Branch history
    try:
        branch_file = data_dir / "branch_history.json"
        with open(branch_file, 'r', encoding='utf-8') as f:
            branches = json.load(f)
        print(f"\nBranch History: {len(branches)} branches")
        for i, branch in enumerate(branches[:3], 1):
            print(f"  {i}. {branch['type']:8} - {branch['description']}")
        if len(branches) > 3:
            print(f"  ... and {len(branches) - 3} more")
    except Exception as e:
        print(f"\nBranch History: Error - {e}")
    
    # CI pipeline
    try:
        pipeline_file = data_dir / "ci_pipeline_timeline.json"
        with open(pipeline_file, 'r', encoding='utf-8') as f:
            pipeline_data = json.load(f)
        history = pipeline_data.get('pipeline_history', [])
        passed = sum(1 for h in history if h['status'] == 'passed')
        failed = len(history) - passed
        print(f"\nCI/CD Pipeline: {len(history)} iterations")
        print(f"  Passed: {passed}, Failed: {failed}")
        if history:
            avg_duration = sum(h['duration'] for h in history) / len(history)
            print(f"  Avg Duration: {avg_duration:.2f}s")
    except Exception as e:
        print(f"\nCI/CD Pipeline: Error - {e}")
    
    # Deployments
    try:
        deploy_file = data_dir / "deployment_history.json"
        with open(deploy_file, 'r', encoding='utf-8') as f:
            deployments = json.load(f)
        print(f"\nDeployments: {len(deployments)} deployments")
        for deploy in deployments:
            print(f"  - {deploy['platform']}: {deploy['status']}")
    except Exception as e:
        print(f"\nDeployments: Error - {e}")
    
    print("\n" + "="*60)


def check_git_ready():
    """Check if git is ready for push"""
    print_step(6, "Checking Git repository status")
    
    # Check if git initialized
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            print("  [ERROR] Not a git repository")
            print("  Run: git init")
            print_step(6, "Checking Git repository status", "FAIL")
            return False
    except Exception as e:
        print(f"  [ERROR] Git check failed: {e}")
        print_step(6, "Checking Git repository status", "FAIL")
        return False
    
    # Check if remote configured
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0 or not result.stdout.strip():
            print("  [WARNING] No remote configured")
            print("  Run: git remote add origin https://github.com/USERNAME/RIFT26.git")
            print_step(6, "Checking Git repository status", "FAIL")
            return False
        else:
            # Show remote
            remotes = result.stdout.strip().split('\n')
            print(f"  Remote: {remotes[0]}")
    except Exception as e:
        print(f"  [WARNING] Remote check failed: {e}")
    
    print_step(6, "Checking Git repository status", "OK")
    return True


def prepare_git_commit():
    """Stage files and prepare commit"""
    print_step(7, "Preparing Git commit")
    
    try:
        # Stage data files
        subprocess.run(["git", "add", "data/"], check=True, timeout=10)
        
        # Check what's staged
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        staged_files = result.stdout.strip().split('\n')
        staged_files = [f for f in staged_files if f]
        
        if not staged_files:
            print("  [INFO] No changes to commit")
            print_step(7, "Preparing Git commit", "SKIP")
            return False
        
        print(f"  Staged {len(staged_files)} file(s):")
        for f in staged_files:
            print(f"    - {f}")
        
        # Create commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"[AI-AGENT] Production Update: DevOps automation data - {timestamp}"
        
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, timeout=10)
        
        print(f"  Commit message: {commit_msg}")
        print_step(7, "Preparing Git commit", "OK")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Git command failed: {e}")
        print_step(7, "Preparing Git commit", "FAIL")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        print_step(7, "Preparing Git commit", "FAIL")
        return False


def push_to_github():
    """Push changes to GitHub"""
    print_step(8, "Pushing to GitHub")
    
    # Get current branch
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5
        )
        branch = result.stdout.strip() or "main"
    except:
        branch = "main"
    
    print(f"  Target branch: {branch}")
    print(f"\n  This will push your changes to GitHub.")
    
    # Confirm
    response = input("  Push to GitHub? [y/N]: ").strip().lower()
    
    if response != 'y':
        print("  [CANCELLED] Push cancelled by user")
        print_step(8, "Pushing to GitHub", "SKIP")
        return False
    
    try:
        result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("  [SUCCESS] Pushed to GitHub!")
            print_step(8, "Pushing to GitHub", "OK")
            return True
        else:
            print(f"  [ERROR] Push failed:")
            print(f"  {result.stderr}")
            print_step(8, "Pushing to GitHub", "FAIL")
            return False
            
    except Exception as e:
        print(f"  [ERROR] {e}")
        print_step(8, "Pushing to GitHub", "FAIL")
        return False


def main():
    """Main production test workflow"""
    print("\n" + "="*60)
    print("PRODUCTION-READY GITHUB INTEGRATION TEST")
    print("Member 2 - DevOps/Git Automation Lead")
    print("="*60)
    
    # Step 1: Clean old data
    clean_data_files()
    
    # Step 2: Generate branch data
    branches = generate_branch_data(count=8)
    if not branches:
        print("\n[ABORT] Failed to generate branch data")
        return 1
    
    # Step 3: Generate CI pipeline data
    pipeline_results = generate_ci_pipeline_data(iterations=5)
    if not pipeline_results:
        print("\n[ABORT] Failed to generate CI pipeline data")
        return 1
    
    # Step 4: Generate deployment data
    deployments = generate_deployment_data()
    
    # Step 5: Verify all data
    if not verify_data_files():
        print("\n[ABORT] Data validation failed")
        return 1
    
    # Show summary
    show_data_summary()
    
    # Step 6-8: Git workflow
    print("\n" + "="*60)
    print("GIT WORKFLOW")
    print("="*60)
    
    if not check_git_ready():
        print("\n[INFO] Git not ready. Setup required.")
        print("\nSee GITHUB_INTEGRATION_GUIDE.md for setup instructions")
        return 0
    
    if prepare_git_commit():
        push_to_github()
    
    print("\n" + "="*60)
    print("[COMPLETE] Production test finished!")
    print("="*60)
    print("\nYour data files are ready for the hackathon demo!")
    print("Check: data/ folder for all generated JSON files")
    print("\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
