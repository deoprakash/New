"""
Git Automation with GitPython
Automated commit and push flow for CI/CD pipeline
"""

import os
import sys
from git import Repo, GitCommandError
from pathlib import Path
import logging
from datetime import datetime
import json
from branch_manager import BranchManager

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"git_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class GitAutomation:
    """Automates Git operations including commit and push flows"""
    
    def __init__(self, repo_path="."):
        """
        Initialize Git Automation
        
        Args:
            repo_path (str): Path to Git repository
        """
        try:
            self.repo_path = Path(repo_path).resolve()
            self.repo = Repo(repo_path)
            self.branch_manager = BranchManager(repo_path)
            logger.info(f"Initialized Git automation for: {self.repo_path}")

            self.team_name = os.getenv("TEAM_NAME", "RIFT_ORGANISERS")
            self.leader_name = os.getenv("LEADER_NAME", "SAIYAM_KUMAR")
            
            # Setup data directory
            self.data_dir = self.repo_path / "data"
            self.data_dir.mkdir(exist_ok=True)
            self.history_file = self.data_dir / "git_automation_history.json"
            
            # Initialize file if doesn't exist
            if not self.history_file.exists():
                self.history_file.write_text("[]", encoding='utf-8')
            
            self.automation_history = []
            
        except Exception as e:
            logger.error(f"Failed to initialize repository: {e}")
            raise
    
    def check_status(self):
        """
        Check repository status
        
        Returns:
            dict: Status information
        """
        try:
            status = {
                "branch": self.repo.active_branch.name,
                "modified": [item.a_path for item in self.repo.index.diff(None)],
                "untracked": self.repo.untracked_files,
                "staged": [item.a_path for item in self.repo.index.diff("HEAD")],
                "clean": not self.repo.is_dirty(untracked_files=True)
            }
            
            logger.info(f"Repository status: {status['branch']}")
            logger.info(f"  Modified: {len(status['modified'])}")
            logger.info(f"  Untracked: {len(status['untracked'])}")
            logger.info(f"  Staged: {len(status['staged'])}")
            logger.info(f"  Clean: {status['clean']}")
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to check status: {e}")
            return None
    
    def add_files(self, files=None, add_all=False):
        """
        Stage files for commit
        
        Args:
            files (list, optional): List of files to add
            add_all (bool): Add all changes
            
        Returns:
            bool: Success status
        """
        try:
            if add_all:
                logger.info("Staging all changes...")
                self.repo.git.add(A=True)
            elif files:
                logger.info(f"Staging {len(files)} files...")
                self.repo.index.add(files)
            else:
                logger.warning("No files specified to add")
                return False
            
            logger.info("[OK] Files staged successfully")
            return True
            
        except Exception as e:
            logger.error(f"[FAIL] Failed to stage files: {e}")
            return False
    
    def commit(self, message, author_name=None, author_email=None):
        """
        Commit staged changes
        
        Args:
            message (str): Commit message
            author_name (str, optional): Author name
            author_email (str, optional): Author email
            
        Returns:
            str: Commit hash if successful, None otherwise
        """
        try:
            # Check if there are changes to commit
            if not self.repo.is_dirty():
                logger.warning("No changes to commit")
                return None
            
            if not message.startswith("[AI-AGENT]"):
                message = f"[AI-AGENT] {message}"

            logger.info(f"Committing changes: {message[:50]}...")
            
            # Set author if provided
            if author_name and author_email:
                commit = self.repo.index.commit(
                    message,
                    author=f"{author_name} <{author_email}>"
                )
            else:
                commit = self.repo.index.commit(message)
            
            commit_hash = commit.hexsha[:7]
            logger.info(f"[OK] Commit successful: {commit_hash}")
            
            # Record commit
            commit_record = {
                "timestamp": datetime.now().isoformat(),
                "action": "commit",
                "commit_hash": commit_hash,
                "message": message,
                "branch": self.repo.active_branch.name
            }
            self.automation_history.append(commit_record)
            self._save_operation(commit_record)
            
            return commit_hash
            
        except Exception as e:
            logger.error(f"[FAIL] Commit failed: {e}")
            return None
    
    def push(self, remote="origin", branch=None, force=False):
        """
        Push commits to remote repository
        
        Args:
            remote (str): Remote name
            branch (str, optional): Branch to push (current branch if None)
            force (bool): Force push
            
        Returns:
            bool: Success status
        """
        try:
            if branch is None:
                branch = self.repo.active_branch.name
            
            if branch in ["main", "master"]:
                logger.error("[FAIL] Push blocked: refusing to push directly to main/master")
                return False

            logger.info(f"Pushing to {remote}/{branch}...")
            
            if force:
                logger.warning("Force push enabled")
                self.repo.remotes[remote].push(branch, force=True)
            else:
                self.repo.remotes[remote].push(branch)
            
            logger.info(f"[OK] Push successful to {remote}/{branch}")
            
            # Record push
            push_record = {
                "timestamp": datetime.now().isoformat(),
                "action": "push",
                "remote": remote,
                "branch": branch,
                "force": force,
                "status": "success"
            }
            self.automation_history.append(push_record)
            self._save_operation(push_record)
            
            return True
            
        except GitCommandError as e:
            logger.error(f"[FAIL] Push failed: {e}")
            return False
        except Exception as e:
            logger.error(f"[FAIL] Unexpected error during push: {e}")
            return False

    def ensure_ai_fix_branch(self, team_name=None, leader_name=None, base_branch=None):
        """Ensure we are on TEAM_NAME_LEADER_NAME_AI_Fix branch"""
        if base_branch is None:
            base_branch = os.getenv("DEFAULT_BRANCH", "main")
        team_name = team_name or self.team_name
        leader_name = leader_name or self.leader_name

        target_branch = self.branch_manager.generate_branch_name(
            team_name=team_name,
            leader_name=leader_name
        )

        current_branch = self.repo.active_branch.name
        if current_branch == target_branch:
            return target_branch

        created = self.branch_manager.create_branch(
            target_branch,
            base_branch=base_branch,
            checkout=True
        )

        if not created:
            raise RuntimeError("Failed to create or checkout AI fix branch")

        return target_branch
    
    def automated_commit_push(self, message, add_all=True, remote="origin"):
        """
        Automated workflow: add -> commit -> push
        
        Args:
            message (str): Commit message
            add_all (bool): Stage all changes
            remote (str): Remote to push to
            
        Returns:
            dict: Results of automation
        """
        logger.info("=== Starting Automated Commit & Push ===")
        
        results = {
            "add": False,
            "commit": None,
            "push": False,
            "timestamp": datetime.now().isoformat()
        }
        
        # Step 0: Ensure AI fix branch
        try:
            self.ensure_ai_fix_branch()
        except Exception as e:
            logger.error(f"[FAIL] {e}")
            return results

        # Step 1: Add files
        if self.add_files(add_all=add_all):
            results["add"] = True
        else:
            logger.error("Failed to add files, aborting...")
            return results
        
        # Step 2: Commit
        commit_hash = self.commit(message)
        if commit_hash:
            results["commit"] = commit_hash
        else:
            logger.error("Failed to commit, aborting...")
            return results
        
        # Step 3: Push
        if self.push(remote=remote):
            results["push"] = True
        else:
            logger.error("Failed to push")
        
        logger.info("=== Automation Complete ===")
        return results
    
    def pull(self, remote="origin", branch=None):
        """
        Pull latest changes from remote
        
        Args:
            remote (str): Remote name
            branch (str, optional): Branch to pull
            
        Returns:
            bool: Success status
        """
        try:
            if branch is None:
                branch = self.repo.active_branch.name
            
            logger.info(f"Pulling from {remote}/{branch}...")
            self.repo.remotes[remote].pull(branch)
            logger.info("[OK] Pull successful")
            return True
            
        except Exception as e:
            logger.error(f"[FAIL] Pull failed: {e}")
            return False
    
    def create_ai_branch_and_commit(self, description, commit_message, team_name=None, leader_name=None):
        """
        Create TEAM_NAME_LEADER_NAME_AI_Fix branch, commit, and push
        
        Args:
            description (str): Branch description
            commit_message (str): Commit message
            team_name (str, optional): Team name
            leader_name (str, optional): Team leader name
            
        Returns:
            dict: Results of operation
        """
        logger.info("=== AI Branch Creation & Automation ===")
        
        # Create branch
        branch_name = self.branch_manager.create_ai_fix_branch(
            team_name=team_name,
            leader_name=leader_name
        )
        
        if not branch_name:
            logger.error("Failed to create branch")
            return {"success": False, "branch": None}
        
        # Automated commit and push
        results = self.automated_commit_push(commit_message)
        results["branch"] = branch_name
        
        return results
    
    def _save_operation(self, operation):
        """Save operation to history file immediately"""
        try:
            # Read existing history
            existing_history = []
            if self.history_file.exists():
                content = self.history_file.read_text(encoding='utf-8')
                if content.strip():
                    existing_history = json.loads(content)
            
            # Append new operation
            existing_history.append(operation)
            
            # Write back
            self.history_file.write_text(json.dumps(existing_history, indent=2), encoding='utf-8')
            
        except Exception as e:
            logger.error(f"Failed to save automation history: {e}")
    
    def save_automation_history(self):
        """Save automation history to JSON file"""
        try:
            self.history_file.write_text(json.dumps(self.automation_history, indent=2), encoding='utf-8')
            logger.info(f"Automation history saved to {self.history_file}")
        except Exception as e:
            logger.error(f"Failed to save automation history: {e}")


def main():
    """Main execution function"""
    logger.info("=== Git Automation System ===")
    
    try:
        # Initialize automation
        git_auto = GitAutomation()
        
        # Check status
        status = git_auto.check_status()
        
        if status and not status['clean']:
            logger.info("\nRepository has changes. Running automated workflow...")
            
            # Example: Automated commit and push
            results = git_auto.automated_commit_push(
                message="[AI] Automated commit via GitPython automation",
                add_all=True
            )
            
            logger.info("\n=== Results ===")
            logger.info(f"  Add: {'[OK]' if results['add'] else '[FAIL]'}")
            logger.info(f"  Commit: {results['commit'] or '[FAIL]'}")
            logger.info(f"  Push: {'[OK]' if results['push'] else '[FAIL]'}")
        else:
            logger.info("Repository is clean, no changes to commit")
        
        # Save history
        git_auto.save_automation_history()
        
    except Exception as e:
        logger.error(f"Automation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
