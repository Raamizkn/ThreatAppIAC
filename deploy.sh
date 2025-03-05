#!/bin/bash

# Exit on error
set -e

echo "=== Threat Detection App Deployment ==="
echo "This script will deploy the Threat Detection App using Terraform."
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker Desktop first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "Error: Terraform is not installed. Please install Terraform first."
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo "=== Building Docker Image ==="
docker build -t threat-detection-app:latest -f app/Dockerfile app/

echo "=== Initializing Terraform ==="
cd terraform
terraform init

echo "=== Planning Terraform Deployment ==="
terraform plan

echo "=== Applying Terraform Configuration ==="
terraform apply -auto-approve

echo
echo "=== Deployment Complete ==="
echo "The Threat Detection App is now running."
echo "You can access it at: http://localhost:5000"
echo
echo "To stop the application, run: cd terraform && terraform destroy -auto-approve" 