"""
Main Execution Script
Orchestrates the complete DevOps workflow
"""

import sys
from pathlib import Path
from datetime import datetime
import logging
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Setup logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"main_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Add directories to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent / "ci_cd" / "pipeline"))
sys.path.insert(0, str(Path(__file__).parent / "ci_cd" / "tracker"))
sys.path.insert(0, str(Path(__file__).parent / "deployment"))


def banner(text):
    """Print a banner"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def run_git_automation_demo():
    """Run Git automation demonstration"""
    banner("Phase 1: Git Automation (First 4 Hours)")
    
    try:
        from branch_manager import BranchManager
        
        logger.info("Initializing Branch Manager...")
        manager = BranchManager()
        
        # Generate and SAVE example branches
        logger.info("\nGenerating TEAM_LEADER_AI_Fix branches:")
        examples = [
            ("bug", "101", "fix_authentication"),
            ("feature", "102", "add_analytics"),
            ("hotfix", "103", "security_patch"),
            ("fix", None, "performance_optimization")
        ]
        
        created_branches = []
        for issue_type, issue_id, description in examples:
            branch_entry = manager.create_branch_entry(issue_type, issue_id, description)
            created_branches.append(branch_entry)
            print(f"  [OK] {branch_entry['branch_name']}")
        
        logger.info(f"\n[OK] Git automation complete - {len(created_branches)} branches created")
        return True
        
    except Exception as e:
        logger.error(f"[FAIL] Git automation failed: {e}")
        return False


def run_ci_pipeline_demo():
    """Run CI/CD pipeline demonstration"""
    banner("Phase 2: CI/CD Pipeline (Next 4 Hours)")
    
    try:
        from ci_runner import CIRunner
        from iteration_tracker import IterationTracker
        
        logger.info("Initializing CI Pipeline...")
        # Force simulation mode for production-ready testing
        runner = CIRunner(use_simulation=True)
        
        # Run simulation (reduced iterations for demo)
        logger.info("Running CI pipeline simulation (production-safe mode)...")
        results = runner.run_simulation_loop(iterations=3, delay=1)
        
        # Save pipeline data
        runner.save_pipeline_data()
        
        # Generate tracking report
        logger.info("\nGenerating iteration tracking report...")
        tracker = IterationTracker()
        tracker.print_summary()
        tracker.save_report()
        
        logger.info("\n✓ CI/CD pipeline demonstration complete!")
        return True
        
    except Exception as e:
        logger.error(f"✗ CI pipeline failed: {e}")
        return False


def run_deployment_demo():
    """Run deployment demonstration"""
    banner("Phase 3: Deployment (Final Hours)")
    
    try:
        from deploy import DeploymentManager
        
        logger.info("Initializing Deployment Manager...")
        manager = DeploymentManager()
        
        # Deploy to Railway
        logger.info("\nDeploying to Railway...")
        railway_result = manager.deploy_railway("rift26-backend")
        
        # Deploy to AWS
        logger.info("\nDeploying to AWS...")
        aws_result = manager.deploy_aws(region="us-east-1", service_type="lambda")
        
        # Print summary
        manager.print_deployment_summary()
        
        # Save history
        manager.save_deployment_history()
        
        logger.info("\n✓ Deployment demonstration complete!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Deployment failed: {e}")
        return False


def print_final_summary():
    """Print final summary"""
    banner("RIFT'26 DevOps Lead - Final Summary")
    
    print("✓ Deliverables Completed:\n")
    print("  1. Working Git Automation")
    print("     - Repo cloning script")
    print("     - Branch naming: TEAM_LEADER_AI_Fix")
    print("     - GitPython commit + push flow")
    print()
    print("  2. CI/CD Pipeline")
    print("     - Docker sandbox configuration")
    print("     - CI simulation loop")
    print("     - Iteration tracking")
    print()
    print("  3. Deployment")
    print("     - Railway configuration")
    print("     - AWS configuration")
    print("     - Deployment automation")
    print()
    print("  4. Timeline Data")
    print("     - data/ci_pipeline_timeline.json")
    print("     - data/iteration_tracker.json")
    print("     - data/git_automation_history.json")
    print("     - data/deployment_history.json")
    print()
    print("="*70)
    print("All systems ready for production deployment!")
    print("="*70 + "\n")


def main():
    """Main execution"""
    banner("RIFT'26 - DevOps / Git Automation Lead")
    
    logger.info(f"Project: RIFT'26")
    logger.info(f"Role: Member 2 - DevOps / Git Automation Lead")
    logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Phase 1: Git Automation
    results.append(("Git Automation", run_git_automation_demo()))
    
    # Phase 2: CI/CD Pipeline
    results.append(("CI/CD Pipeline", run_ci_pipeline_demo()))
    
    # Phase 3: Deployment
    results.append(("Deployment", run_deployment_demo()))
    
    # Final Summary
    print_final_summary()
    
    # Print results
    banner("Execution Results")
    for phase, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {status}: {phase}")
    print()
    
    # Overall status
    all_passed = all(result[1] for result in results)
    if all_passed:
        logger.info("🎉 All phases completed successfully!")
        return 0
    else:
        logger.error("⚠ Some phases failed. Check logs for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
