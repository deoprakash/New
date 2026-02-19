# Project Configuration

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Git Configuration
GIT_USER_NAME=DevOps Lead
GIT_USER_EMAIL=devops@rift26.com

# Repository Settings
DEFAULT_BRANCH=main
REMOTE_NAME=origin

# CI/CD Configuration
CI_ENVIRONMENT=local
PIPELINE_ITERATIONS=3
PIPELINE_DELAY=5

# Docker Configuration
DOCKER_IMAGE_NAME=rift26-ci
DOCKER_CONTAINER_NAME=rift26-pipeline

# Deployment Configuration
RAILWAY_PROJECT_ID=
RAILWAY_ENVIRONMENT=production

AWS_REGION=us-east-1
AWS_SERVICE_TYPE=lambda
AWS_FUNCTION_NAME=rift26-backend

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs

# Data Directory
DATA_DIR=data
```

## Configuration Files

### Git Configuration (.gitconfig)
```ini
[user]
    name = DevOps Lead
    email = devops@rift26.com

[core]
    autocrlf = input
    
[push]
    default = current
```

### Docker Configuration
See `docker-compose.yml` for service configuration

### CI/CD Configuration
- Pipeline iterations: 3
- Test timeout: 300 seconds
- Build timeout: 600 seconds

## Project Settings

### Branch Naming Convention
- Format: `DEO_PRAKASH_AI_Fix/<type>/<timestamp>[/issue_<id>][/description]`
- Types: bug, feature, hotfix, fix
- Example: `DEO_PRAKASH_AI_Fix/bug/20260219_143022/issue_123/login_fix`

### Commit Message Convention
- Format: `[<type>] <message>`
- Types: AI, FIX, FEAT, HOTFIX, CHORE
- Example: `[AI] Automated commit via GitPython automation`

### Deployment Targets
1. **Railway**
   - Platform: Railway.app
   - Service: rift26-backend
   - Region: Auto

2. **AWS**
   - Platform: AWS
   - Service: Lambda/ECS
   - Region: us-east-1

## Directory Structure

```
RIFT'26/
├── scripts/              # Automation scripts
├── ci_cd/                # CI/CD pipeline
│   ├── docker/          # Docker configurations
│   ├── pipeline/        # Pipeline scripts
│   └── tracker/         # Iteration tracking
├── deployment/          # Deployment configs
│   ├── railway/         # Railway deployment
│   └── aws/            # AWS deployment
├── tests/              # Test suite
├── data/               # Timeline data
├── logs/               # Log files
└── config/             # Configuration files
```
