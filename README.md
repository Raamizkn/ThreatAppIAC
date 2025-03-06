# Containerized Threat Detection App with Infrastructure-as-Code

This project demonstrates a containerized threat detection application deployed using Infrastructure-as-Code (IaC) principles. The application is a Python Flask web service that analyzes text for potential security threats using a simple machine learning model.

## Architecture Overview

The project consists of two major components:

1. **Threat Detection Application**: A Python Flask application that simulates threat detection on incoming email-like data. This application is containerized using Docker.

2. **Infrastructure Provisioning and Deployment**: Infrastructure-as-Code (IaC) using Terraform to define and deploy the containerized app into a simulated cloud environment via local Docker orchestration.

## Project Structure

```
.
├── app/                    # Flask application
│   ├── app.py              # Main application code
│   ├── Dockerfile          # Docker configuration
│   ├── templates/          # HTML templates
│   │   └── index.html      # Web interface
│   └── test_app.py         # Unit tests
├── terraform/              # Terraform configuration
│   ├── main.tf             # Main Terraform configuration
│   ├── variables.tf        # Variable definitions
│   └── outputs.tf          # Output definitions
├── .github/workflows/      # CI/CD configuration
│   └── ci-cd.yml           # GitHub Actions workflow
└── README.md               # Project documentation
```

## Features

- **Threat Detection**: Uses a simple machine learning model to classify text as safe or potentially threatening.
- **RESTful API**: Provides endpoints for individual and batch text analysis.
- **Web Interface**: A user-friendly interface for interacting with the threat detection service.
- **Containerization**: Packaged as a Docker container for consistent deployment.
- **Infrastructure-as-Code**: Uses Terraform to provision and manage infrastructure.
- **CI/CD Pipeline**: Automated testing, building, and deployment using GitHub Actions.

## Prerequisites

- Docker Desktop
- Terraform CLI (>= 1.0.0)
- Python 3.9+
- Git

## Getting Started

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/threat-detection-app.git
   cd threat-detection-app
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application locally:
   ```bash
   cd app
   python app.py
   ```

4. Access the application at http://localhost:5000

### Deployment with Docker and Terraform

1. Initialize Terraform:
   ```bash
   cd terraform
   terraform init
   ```

2. Plan the deployment:
   ```bash
   terraform plan
   ```

3. Apply the configuration:
   ```bash
   terraform apply
   ```

4. Access the deployed application at http://localhost:5000

5. To tear down the infrastructure:
   ```bash
   terraform destroy
   ```

## API Endpoints

- **GET /health**: Health check endpoint
- **POST /api/detect**: Analyze a single text
  ```json
  {
    "text": "Your text to analyze"
  }
  ```
- **POST /api/batch-detect**: Analyze multiple texts
  ```json
  {
    "texts": ["Text 1", "Text 2", "Text 3"]
  }
  ```

## Testing

Run the unit tests:
```bash
pytest app/test_app.py
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:
1. Runs tests on every push and pull request
2. Builds and pushes the Docker image to Docker Hub
3. Applies the Terraform configuration to update the infrastructure

## License

This project is licensed under the proprietary license
