"""
Branch Manager - TEAM_LEADER_AI_Fix naming convention
Handles branch creation, naming, and management
"""

import os
from git import Repo, GitCommandError
from datetime import datetime
import logging
from pathlib import Path
import json

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"branch_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class BranchManager:
    """Manages Git branches with DEO_PRAKASH_AI_Fix naming convention"""
    
    BRANCH_PREFIX = "DEO_PRAKASH_AI"
    
    def __init__(self, repo_path=None):
        """
        Initialize Branch Manager
        
        Args:
            repo_path (str): Path to Git repository
        """
        if repo_path:
            try:
                self.repo = Repo(repo_path)
                logger.info(f"Initialized repo at {repo_path}")
            except Exception as e:
                logger.error(f"Failed to initialize repository: {e}")
                self.repo = None
        else:
            self.repo = None
        
        # Setup data directory
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "branch_history.json"
        
        # Initialize file if doesn't exist
        if not self.history_file.exists():
            self.history_file.write_text("[]", encoding='utf-8')
        
        self.branch_history = []
    
    def generate_branch_name(self, issue_type, issue_id=None, description=None):
        """
        Generate branch name following TEAM_LEADER_AI_Fix convention
        
        Args:
            issue_type (str): Type of fix (bug, feature, hotfix, etc.)
            issue_id (str, optional): Issue/ticket ID
            description (str, optional): Brief description
            
        Returns:
            str: Formatted branch name
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        parts = [self.BRANCH_PREFIX, issue_type, timestamp]
        
        if issue_id:
            parts.append(f"issue_{issue_id}")
        
        if description:
            # Sanitize description for branch name
            clean_desc = description.lower().replace(' ', '_')
            clean_desc = ''.join(c for c in clean_desc if c.isalnum() or c == '_')
            parts.append(clean_desc[:30])  # Limit length
        
        branch_name = "/".join(parts)
        logger.info(f"Generated branch name: {branch_name}")
        return branch_name
    
    def create_branch(self, branch_name, base_branch="main", checkout=True):
        """
        Create a new branch
        
        Args:
            branch_name (str): Name of the new branch
            base_branch (str): Base branch to create from
            checkout (bool): Whether to checkout the new branch
            
        Returns:
            bool: Success status
        """
        if not self.repo:
            logger.error("No repository initialized")
            return False
        
        try:
            # Ensure we're on the base branch
            logger.info(f"Switching to base branch: {base_branch}")
            self.repo.git.checkout(base_branch)
            
            # Pull latest changes
            logger.info("Pulling latest changes...")
            self.repo.remotes.origin.pull()
            
            # Create new branch
            logger.info(f"Creating branch: {branch_name}")
            new_branch = self.repo.create_head(branch_name)
            
            if checkout:
                logger.info(f"Checking out branch: {branch_name}")
                new_branch.checkout()
            
            # Record branch creation
            branch_record = {
                "timestamp": datetime.now().isoformat(),
                "branch_name": branch_name,
                "base_branch": base_branch,
                "status": "created"
            }
            self.branch_history.append(branch_record)
            
            logger.info(f"✓ Successfully created branch: {branch_name}")
            return True
            
        except GitCommandError as e:
            logger.error(f"✗ Git command failed: {e}")
            return False
        except Exception as e:
            logger.error(f"✗ Unexpected error: {e}")
            return False
    
    def create_ai_fix_branch(self, issue_type="fix", issue_id=None, description=None):
        """
        Create a branch using the TEAM_LEADER_AI_Fix naming convention
        
        Args:
            issue_type (str): Type of fix
            issue_id (str, optional): Issue ID
            description (str, optional): Description
            
        Returns:
            str: Branch name if successful, None otherwise
        """
        branch_name = self.generate_branch_name(issue_type, issue_id, description)
        
        if self.create_branch(branch_name):
            return branch_name
        return None
    
    def list_branches(self, pattern=None):
        """
        List branches in the repository
        
        Args:
            pattern (str, optional): Filter branches by pattern
            
        Returns:
            list: List of branch names
        """
        if not self.repo:
            logger.error("No repository initialized")
            return []
        
        try:
            branches = [branch.name for branch in self.repo.heads]
            
            if pattern:
                branches = [b for b in branches if pattern in b]
            
            logger.info(f"Found {len(branches)} branches")
            return branches
            
        except Exception as e:
            logger.error(f"Failed to list branches: {e}")
            return []
    
    def delete_branch(self, branch_name, force=False):
        """
        Delete a branch
        
        Args:
            branch_name (str): Name of branch to delete
            force (bool): Force deletion
            
        Returns:
            bool: Success status
        """
        if not self.repo:
            logger.error("No repository initialized")
            return False
        
        try:
            self.repo.delete_head(branch_name, force=force)
            logger.info(f"✓ Deleted branch: {branch_name}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to delete branch: {e}")
            return False
    
    def get_current_branch(self):
        """Get the current active branch name"""
        if not self.repo:
            return None
        
        try:
            return self.repo.active_branch.name
        except Exception as e:
            logger.error(f"Failed to get current branch: {e}")
            return None
    
    def create_branch_entry(self, issue_type, issue_id=None, description=None):
        """Create and save a branch entry"""
        branch_name = self.generate_branch_name(issue_type, issue_id, description)
        
        branch_entry = {
            "branch_name": branch_name,
            "type": issue_type,
            "timestamp": datetime.now().isoformat(),
            "issue_id": issue_id or "N/A",
            "description": description or "N/A",
            "created_by": "DevOps_Lead",
            "status": "created"
        }
        
        self.branch_history.append(branch_entry)
        
        # Immediately save to file
        self._save_to_file(branch_entry)
        
        return branch_entry
    
    def _save_to_file(self, branch_entry):
        """Save branch entry to JSON file"""
        try:
            # Read existing history
            existing_history = []
            if self.history_file.exists():
                content = self.history_file.read_text(encoding='utf-8')
                if content.strip():
                    existing_history = json.loads(content)
            
            # Append new entry
            existing_history.append(branch_entry)
            
            # Write back
            self.history_file.write_text(json.dumps(existing_history, indent=2), encoding='utf-8')
            logger.info(f"Branch saved: {branch_entry['branch_name']}")
            
        except Exception as e:
            logger.error(f"Failed to save branch history: {e}")
    
    def save_branch_history(self):
        """Save branch history to JSON file (for compatibility)"""
        try:
            self.history_file.write_text(json.dumps(self.branch_history, indent=2), encoding='utf-8')
            logger.info(f"Branch history saved to {self.history_file}")
        except Exception as e:
            logger.error(f"Failed to save branch history: {e}")


def main():
    """Main execution function"""
    logger.info("=== Branch Manager - TEAM_LEADER_AI_Fix ===")
    
    # Example usage
    manager = BranchManager()
    
    # Generate example branch names
    examples = [
        ("bug", "123", "fix_login_issue"),
        ("feature", "456", "add_dashboard"),
        ("hotfix", "789", "critical_security_patch"),
        ("fix", None, "improve_performance")
    ]
    
    logger.info("\n=== Example Branch Names ===")
    for issue_type, issue_id, description in examples:
        branch_name = manager.generate_branch_name(issue_type, issue_id, description)
        logger.info(f"  {branch_name}")
    
    # Save history
    manager.save_branch_history()
    
    logger.info("\n=== Branch Manager Complete ===")


if __name__ == "__main__":
    main()
