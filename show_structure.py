"""
Project Structure Visualizer
Displays the complete project structure
"""

from pathlib import Path
from datetime import datetime

def print_tree(directory, prefix="", max_depth=None, current_depth=0, ignore_dirs=None):
    """Print directory tree structure"""
    if ignore_dirs is None:
        ignore_dirs = {'__pycache__', '.git', 'venv', '.venv', 'node_modules'}
    
    if max_depth and current_depth >= max_depth:
        return
    
    try:
        entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        dirs = [e for e in entries if e.is_dir() and e.name not in ignore_dirs]
        files= [e for e in entries if e.is_file()]
        
        all_entries = dirs + files
        
        for idx, entry in enumerate(all_entries):
            is_last = idx == len(all_entries) - 1
            
            if entry.is_dir():
                print(f"{prefix}{'└── ' if is_last else '├── '}📁 {entry.name}/")
                extension = "    " if is_last else "│   "
                print_tree(entry, prefix + extension, max_depth, current_depth + 1, ignore_dirs)
            else:
                # File icons based on extension
                icon = "📄"
                if entry.suffix in ['.py']:
                    icon = "🐍"
                elif entry.suffix in ['.md', '.txt']:
                    icon = "📄"
                elif entry.suffix in ['.json', '.yml', '.yaml']:
                    icon = "⚙️"
                elif entry.suffix in ['.sh', '.bat']:
                    icon = "📜"
                elif entry.name in ['Dockerfile', '.gitignore', '.env.example']:
                    icon = "⚙️"
                
                print(f"{prefix}{'└── ' if is_last else '├── '}{icon} {entry.name}")
                
    except PermissionError:
        pass


def print_statistics(root_dir):
    """Print project statistics"""
    python_files = list(root_dir.rglob("*.py"))
    config_files = list(root_dir.rglob("*.json")) + list(root_dir.rglob("*.yml")) + list(root_dir.rglob("*.yaml"))
    doc_files = list(root_dir.rglob("*.md"))
    test_files = [f for f in python_files if 'test' in f.name]
    
    print("\n📊 PROJECT STATISTICS")
    print("="*70)
    print(f"Python Files:        {len(python_files)}")
    print(f"Test Files:          {len(test_files)}")
    print(f"Config Files:        {len(config_files)}")
    print(f"Documentation Files: {len(doc_files)}")
    print(f"Total Files:         {len(list(root_dir.rglob('*.*')))}")
    print("="*70)


def main():
    """Main execution"""
    root = Path(__file__).parent
    
    print("="*70)
    print("  RIFT'26 - DevOps / Git Automation Lead")
    print("  Project Structure")
    print("="*70)
    print(f"\n📦 Project Root: {root.name}/\n")
    
    print_tree(root, max_depth=4)
    
    print_statistics(root)
    
    print("\n✅ DELIVERABLES")
    print("="*70)
    print("[OK] Working Git Automation")
    print("  - Repo cloning script")
    print("  - Branch naming: TEAM_NAME_LEADER_NAME_AI_Fix")
    print("  - GitPython commit + push flow")
    print()
    print("[OK] CI/CD Timeline Data")
    print("  - Pipeline runner")
    print("  - Iteration tracking")
    print("  - Docker sandbox")
    print()
    print("[OK] Deployment Configurations")
    print("  - Railway deployment")
    print("  - AWS deployment")
    print("  - Automated deployment flow")
    print("="*70)
    
    print("\n🚀 QUICK START")
    print("="*70)
    print("1. Run quick start:    python quickstart.py")
    print("2. Run main workflow:  python main.py")
    print("3. Run tests:          pytest tests/ -v")
    print("4. Docker build:       docker-compose build")
    print("5. Docker run:         docker-compose up ci-pipeline")
    print("="*70)
    
    print(f"\n⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


if __name__ == "__main__":
    main()
