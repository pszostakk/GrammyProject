#!/bin/bash

# Quick CDK Deploy Script
# Builds Docker image, runs frontend build, and deploys with CDK
# Works on Windows (Git Bash/WSL), macOS, and Linux

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

NO_PROMPT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-prompt)
            NO_PROMPT=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${CYAN}🚀 Starting Quick CDK Deploy...${NC}"

# Step 1: Build Docker image
echo -e "\n${YELLOW}📦 Building Docker image...${NC}"
cd frontend
docker build -t grammy .

# Step 2: Run container and build frontend
echo -e "\n${YELLOW}🏗️  Running frontend build in Docker...${NC}"
FRONTEND_PATH=$(pwd -W)
docker run --rm -v "${FRONTEND_PATH}/dist:/out" grammy sh -c "npm run build && cp -r dist/* /out"
echo -e "${GREEN}✅ Frontend built successfully${NC}"
cd ..

# Step 3: Deploy with CDK
echo -e "\n${YELLOW}🌥️  Running CDK deploy...${NC}"
cd infrastructure/grammy

if [ "$NO_PROMPT" = true ]; then
    cdk deploy --require-approval=never
else
    cdk deploy GrammyDataStack GrammyBackendStack GrammyFrontendStack
fi

cd ../..

echo -e "\n${GREEN}✅ Deployment completed successfully!${NC}"
