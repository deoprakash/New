# RIFT'26 DevOps / Git Automation Lead
# Usage Guide

## Quick Start

### Option 1: Quick Start Script
```bash
python quickstart.py
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run main workflow
python main.py
```

## Individual Component Execution

### Git Automation
```bash
# Repository cloning
python scripts/repo_clone.py

# Branch management
python scripts/branch_manager.py

# Git automation
python scripts/git_automation.py
```

### CI/CD Pipeline
```bash
# Run CI pipeline
python ci_cd/pipeline/ci_runner.py

# View iteration tracking
python ci_cd/tracker/iteration_tracker.py

# Docker sandbox
python ci_cd/docker/sandbox_manager.py
```

### Deployment
```bash
# Deploy to Railway/AWS
python deployment/deploy.py
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_git_automation.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Docker Usage

### Build and Run
```bash
# Build images
docker-compose build

# Run CI pipeline
docker-compose up ci-pipeline

# Run pytest
docker-compose run --rm pytest-runner

# Run git automation
docker-compose run --rm git-automation
```

### Cleanup
```bash
docker-compose down
```

## Project Structure

```
RIFT'26/
├── main.py                 # Main orchestration script
├── quickstart.py           # Quick start script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose config
│
├── scripts/                # Git automation scripts
│   ├── repo_clone.py       # Repository cloning
│   ├── branch_manager.py   # Branch naming (TEAM_NAME_LEADER_NAME_AI_Fix)
│   └── git_automation.py   # Commit + push automation
│
├── ci_cd/                  # CI/CD pipeline
│   ├── pipeline/
│   │   └── ci_runner.py    # CI pipeline runner
│   ├── tracker/
│   │   └── iteration_tracker.py  # Iteration tracking
│   └── docker/
│       └── sandbox_manager.py    # Docker sandbox
│
├── deployment/             # Deployment configurations
│   ├── deploy.py           # Deployment manager
│   ├── railway/            # Railway configs
│   └── aws/                # AWS configs
│
├── tests/                  # Test suite
│   ├── test_git_automation.py
│   ├── test_ci_pipeline.py
│   └── test_deployment.py
│
├── data/                   # Generated timeline data
├── logs/                   # Application logs
└── config/                 # Configuration files
```

## Timeline & Phases

### Phase 1: First 4 Hours - Git Automation
- ✓ Repo cloning script
- ✓ Branch naming: TEAM_NAME_LEADER_NAME_AI_Fix
- ✓ GitPython commit + push flow

### Phase 2: Next 4 Hours - CI/CD Pipeline
- ✓ Docker sandbox
- ✓ CI simulation loop
- ✓ Iteration tracking

### Phase 3: Final Hours - Deployment
- ✓ Railway deployment
- ✓ AWS deployment
- ✓ Branch push verification

## Output Files

After running, check these files:
- `data/ci_pipeline_timeline.json` - CI/CD timeline data
- `data/iteration_tracker.json` - Iteration tracking report
- `data/git_automation_history.json` - Git automation history
- `data/deployment_history.json` - Deployment history
- `logs/*.log` - Detailed logs

## Troubleshooting

### Git Issues
- Ensure Git is installed and configured
- Check Git credentials
- Verify repository access

### Docker Issues
- Ensure Docker Desktop is running
- Check Docker version: `docker --version`
- Verify docker-compose is available

### Python Issues
- Python 3.9+ required
- Install all dependencies from requirements.txt
- Use virtual environment to avoid conflicts

## Support

For issues or questions, check:
1. Log files in `logs/` directory
2. README.md for project overview
3. config/project_config.md for configuration details
