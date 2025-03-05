terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
  required_version = ">= 1.0.0"
}

provider "docker" {
  host = var.docker_host
}

# Build the Docker image for the threat detection app
resource "docker_image" "threat_detection_app" {
  name = "${var.app_name}:${var.app_image_tag}"
  build {
    context    = "${path.module}/../app"
    dockerfile = "${path.module}/../app/Dockerfile"
    tag        = ["${var.app_name}:${var.app_image_tag}"]
  }
  force_remove = true
}

# Create a Docker network
resource "docker_network" "threat_detection_network" {
  name = "${var.app_name}-network"
  driver = "bridge"
}

# Deploy the threat detection app container
resource "docker_container" "threat_detection_app" {
  name  = var.app_name
  image = docker_image.threat_detection_app.image_id
  
  ports {
    internal = var.app_port
    external = var.external_port
  }
  
  networks_advanced {
    name = docker_network.threat_detection_network.name
  }
  
  restart = var.restart_policy
  
  # Mount a volume for logs
  volumes {
    container_path = "/app/logs"
    host_path      = "${path.module}/../logs"
  }
  
  # Health check
  healthcheck {
    test         = ["CMD", "curl", "-f", "http://localhost:${var.app_port}/health"]
    interval     = var.health_check_interval
    timeout      = var.health_check_timeout
    start_period = "5s"
    retries      = var.health_check_retries
  }
  
  # Environment variables
  env = [
    "FLASK_APP=app.py",
    "FLASK_DEBUG=False",
    "PORT=${var.app_port}"
  ]
} 