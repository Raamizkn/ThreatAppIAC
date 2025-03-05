#!/bin/bash

# Exit on error
set -e

echo "=== Threat Detection App Cleanup ==="
echo "This script will destroy the Threat Detection App infrastructure."
echo

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "Error: Terraform is not installed. Please install Terraform first."
    exit 1
fi

echo "=== Destroying Terraform Infrastructure ==="
cd terraform
terraform destroy -auto-approve

echo
echo "=== Cleanup Complete ==="
echo "The Threat Detection App infrastructure has been destroyed." 