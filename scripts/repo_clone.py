"""
Repository Cloning Script
Automates the cloning of repositories for CI/CD pipeline
"""

import os
import sys
import argparse
from git import Repo, GitCommandError
from pathlib import Path
import logging
from datetime import datetime
import json

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"repo_clone_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class RepoCloner:
    """Handles repository cloning operations"""
    
    def __init__(self, base_dir="./repos"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.clone_history = []
        
    def clone_repository(self, repo_url, branch=None, depth=None):
        """
        Clone a repository with specified options
        
        Args:
            repo_url (str): Git repository URL
            branch (str, optional): Specific branch to clone
            depth (int, optional): Clone depth for shallow cloning
            
        Returns:
            Repo: GitPython Repo object
        """
        try:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            clone_path = self.base_dir / repo_name
            
            # Remove existing directory if it exists
            if clone_path.exists():
                logger.warning(f"Repository {repo_name} already exists. Removing...")
                import shutil
                shutil.rmtree(clone_path)
            
            logger.info(f"Cloning repository: {repo_url}")
            logger.info(f"Destination: {clone_path}")
            
            # Clone options
            clone_kwargs = {}
            if branch:
                clone_kwargs['branch'] = branch
                logger.info(f"Cloning branch: {branch}")
            if depth:
                clone_kwargs['depth'] = depth
                logger.info(f"Shallow clone with depth: {depth}")
            
            # Perform clone
            repo = Repo.clone_from(repo_url, clone_path, **clone_kwargs)
            
            # Record clone operation
            clone_record = {
                "timestamp": datetime.now().isoformat(),
                "repo_url": repo_url,
                "repo_name": repo_name,
                "branch": branch or "default",
                "status": "success",
                "path": str(clone_path)
            }
            self.clone_history.append(clone_record)
            
            logger.info(f"[OK] Successfully cloned {repo_name}")
            return repo
            
        except GitCommandError as e:
            logger.error(f"[FAIL] Git command failed: {e}")
            clone_record = {
                "timestamp": datetime.now().isoformat(),
                "repo_url": repo_url,
                "status": "failed",
                "error": str(e)
            }
            self.clone_history.append(clone_record)
            raise
            
        except Exception as e:
            logger.error(f"[FAIL] Unexpected error during cloning: {e}")
            raise
    
    def clone_multiple(self, repo_list):
        """
        Clone multiple repositories
        
        Args:
            repo_list (list): List of dicts with repo_url, branch, depth
        """
        results = []
        for repo_config in repo_list:
            try:
                repo = self.clone_repository(
                    repo_config.get('url'),
                    branch=repo_config.get('branch'),
                    depth=repo_config.get('depth')
                )
                results.append({
                    "repo": repo_config.get('url'),
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "repo": repo_config.get('url'),
                    "status": "failed",
                    "error": str(e)
                })
        
        return results
    
    def save_clone_history(self):
        """Save clone history to JSON file"""
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        
        history_file = data_dir / "clone_history.json"
        with open(history_file, 'w') as f:
            json.dump(self.clone_history, f, indent=2)
        
        logger.info(f"Clone history saved to {history_file}")
        
    def get_repo_info(self, repo_path):
        """Get information about a cloned repository"""
        try:
            repo = Repo(repo_path)
            return {
                "active_branch": repo.active_branch.name,
                "remote_url": repo.remotes.origin.url if repo.remotes else None,
                "last_commit": {
                    "hash": repo.head.commit.hexsha[:7],
                    "message": repo.head.commit.message.strip(),
                    "author": str(repo.head.commit.author),
                    "date": repo.head.commit.committed_datetime.isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Failed to get repo info: {e}")
            return None


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Clone a GitHub repository")
    parser.add_argument("--url", help="GitHub repository URL")
    parser.add_argument("--branch", help="Branch to clone", default=None)
    parser.add_argument("--depth", help="Shallow clone depth", type=int, default=None)
    parser.add_argument("--base-dir", help="Base directory for clones", default="./repos")
    args = parser.parse_args()

    logger.info("=== Repository Cloning Script ===")

    repo_url = args.url
    if not repo_url:
        repo_url = input("Enter GitHub repository URL to clone: ").strip()

    if not repo_url:
        logger.error("[FAIL] No repository URL provided")
        return

    # Initialize cloner
    cloner = RepoCloner(base_dir=args.base_dir)

    # Clone single repository
    try:
        cloner.clone_repository(repo_url, branch=args.branch, depth=args.depth)
        logger.info("\n=== Clone Results ===")
        logger.info(f"[OK] {repo_url}: success")
    except Exception as e:
        logger.info("\n=== Clone Results ===")
        logger.error(f"[FAIL] {repo_url}: {e}")

    # Save history
    cloner.save_clone_history()
    
    logger.info("\n=== Cloning Complete ===")


if __name__ == "__main__":
    main()
