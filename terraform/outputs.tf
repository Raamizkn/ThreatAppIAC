output "app_url" {
  description = "URL to access the threat detection application"
  value       = "http://localhost:${var.external_port}"
}

output "container_id" {
  description = "ID of the Docker container"
  value       = docker_container.threat_detection_app.id
}

output "container_name" {
  description = "Name of the Docker container"
  value       = docker_container.threat_detection_app.name
}

output "image_id" {
  description = "ID of the Docker image"
  value       = docker_image.threat_detection_app.image_id
}

output "network_id" {
  description = "ID of the Docker network"
  value       = docker_network.threat_detection_network.id
}

output "network_name" {
  description = "Name of the Docker network"
  value       = docker_network.threat_detection_network.name
} 