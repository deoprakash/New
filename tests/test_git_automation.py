"""
Test suite for Git Automation
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from branch_manager import BranchManager


class TestBranchManager:
    """Tests for BranchManager"""
    
    def test_generate_branch_name_basic(self):
        """Test basic branch name generation"""
        manager = BranchManager()
        branch_name = manager.generate_branch_name("Code Warriors", "John Doe")
        
        assert branch_name == "CODE_WARRIORS_JOHN_DOE_AI_Fix"
    
    def test_generate_branch_name_with_issue(self):
        """Test branch name with team and leader names"""
        manager = BranchManager()
        branch_name = manager.generate_branch_name("RIFT ORGANISERS", "Saiyam Kumar")
        
        assert branch_name == "RIFT_ORGANISERS_SAIYAM_KUMAR_AI_Fix"
    
    def test_generate_branch_name_with_description(self):
        """Test branch name with extra spaces"""
        manager = BranchManager()
        branch_name = manager.generate_branch_name("  Team One ", " Leader One ")
        
        assert branch_name == "TEAM_ONE_LEADER_ONE_AI_Fix"
    
    def test_generate_branch_name_full(self):
        """Test branch name with special characters"""
        manager = BranchManager()
        branch_name = manager.generate_branch_name("RIFT@2026", "John-Doe")
        
        assert branch_name == "RIFT2026_JOHNDOE_AI_Fix"
    
    def test_branch_prefix_constant(self):
        """Test branch suffix constant"""
        assert BranchManager.BRANCH_SUFFIX == "AI_Fix"


class TestGitAutomation:
    """Tests for Git Automation"""
    
    def test_import_git_automation(self):
        """Test that git_automation module can be imported"""
        from git_automation import GitAutomation
        assert GitAutomation is not None
    
    def test_import_repo_clone(self):
        """Test that repo_clone module can be imported"""
        from repo_clone import RepoCloner
        assert RepoCloner is not None


def test_project_structure():
    """Test that project structure is correct"""
    project_root = Path(__file__).parent.parent
    
    # Check key directories exist
    assert (project_root / "scripts").exists()
    assert (project_root / "ci_cd").exists()
    assert (project_root / "deployment").exists()
    assert (project_root / "tests").exists()
    
    # Check key files exist
    assert (project_root / "README.md").exists()
    assert (project_root / "requirements.txt").exists()
    assert (project_root / "Dockerfile").exists()


def test_branch_naming_convention():
    """Test branch naming follows TEAM_NAME_LEADER_NAME_AI_Fix convention"""
    manager = BranchManager()

    test_cases = [
        ("RIFT ORGANISERS", "Saiyam Kumar", "RIFT_ORGANISERS_SAIYAM_KUMAR_AI_Fix"),
        ("Code Warriors", "John Doe", "CODE_WARRIORS_JOHN_DOE_AI_Fix"),
        ("Team One", "Leader One", "TEAM_ONE_LEADER_ONE_AI_Fix"),
    ]
    
    for team_name, leader_name, expected in test_cases:
        branch_name = manager.generate_branch_name(team_name, leader_name)
        assert branch_name == expected
        print(f"[OK] Generated: {branch_name}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
