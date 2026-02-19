# RIFT'26 - DevOps & Git Automation Lead

## Project Overview
Automated CI/CD pipeline with Git automation, Docker sandboxing, and deployment orchestration.

## Team Member: DevOps / Git Automation Lead

### Timeline & Goals

#### First 4 Hours
- ✅ Repo cloning script
- ✅ Branch naming function: `TEAM_NAME_LEADER_NAME_AI_Fix`
- ✅ GitPython commit + push flow

#### Next 4 Hours
- ✅ Docker sandbox: `docker run pytest`
- ✅ CI simulation loop
- ✅ Iteration tracking for timeline

#### Final Hours
- ✅ Deploy backend (Railway/AWS)
- ✅ Ensure branch pushes correctly

## Deliverables
1. Working Git automation
2. CI/CD timeline data
3. Automated deployment pipeline

## Project Structure
```
├── scripts/              # Automation scripts
│   ├── repo_clone.py     # Repository cloning automation
│   ├── branch_manager.py # Branch naming & management
│   └── git_automation.py # GitPython commit/push flow
│
├── ci_cd/                # CI/CD pipeline
│   ├── docker/           # Docker configurations
│   ├── pipeline/         # CI simulation scripts
│   └── tracker/          # Iteration tracking
│
├── deployment/           # Deployment configurations
│   ├── railway/          # Railway deployment
│   └── aws/              # AWS deployment
│
├── tests/                # Test suite
├── data/                 # CI/CD timeline data
├── config/               # Configuration files
└── logs/                 # Automation logs
```

## Quick Start

### Setup
```bash
pip install -r requirements.txt
```

### Run Git Automation
```bash
python scripts/git_automation.py
```

### Run CI/CD Pipeline
```bash
python ci_cd/pipeline/ci_runner.py
```

### Deploy
```bash
python deployment/deploy.py
```

## Technologies
- Python 3.9+
- GitPython
- Docker
- pytest
- Railway/AWS
