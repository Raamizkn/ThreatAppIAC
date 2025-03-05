variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "threat-detection-app"
}

variable "app_port" {
  description = "Port on which the application runs"
  type        = number
  default     = 5000
}

variable "external_port" {
  description = "External port to expose the application"
  type        = number
  default     = 5000
}

variable "docker_host" {
  description = "Docker host socket"
  type        = string
  default     = "unix:///var/run/docker.sock"
}

variable "app_image_tag" {
  description = "Tag for the Docker image"
  type        = string
  default     = "latest"
}

variable "restart_policy" {
  description = "Container restart policy"
  type        = string
  default     = "always"
}

variable "health_check_interval" {
  description = "Interval between health checks"
  type        = string
  default     = "30s"
}

variable "health_check_timeout" {
  description = "Timeout for health checks"
  type        = string
  default     = "10s"
}

variable "health_check_retries" {
  description = "Number of retries for health checks"
  type        = number
  default     = 3
} 