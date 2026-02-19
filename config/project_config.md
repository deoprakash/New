# Project Configuration

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Git Configuration
GIT_USER_NAME=DevOps Lead
GIT_USER_EMAIL=devops@rift26.com

# Team Branding (Branch Naming)
TEAM_NAME=RIFT ORGANISERS
LEADER_NAME=Saiyam Kumar

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
- Format: `TEAM_NAME_LEADER_NAME_AI_Fix`
- All UPPERCASE
- Spaces replaced with underscores
- Only underscores allowed as special characters
- Example: `RIFT_ORGANISERS_SAIYAM_KUMAR_AI_Fix`

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
