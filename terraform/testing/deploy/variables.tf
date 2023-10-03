variable "resource_group_location" {
  default     = "germanywestcentral"
  description = "Location of the resource group."
}

variable "resource_group_name" {
  default     = "taro-test-env"
  description = "The resource group name."
}

variable "environment" {
  default = "test"
}

variable "acr_name" {
  default = "taroTestContainerRegistry"
}

variable "instance_name" {
  default = "taro-test-api-instance"
}

variable "image_registry_credential_user" {
  default = "user"
}

variable "image_registry_credential_password" {
  default = "secret"
}

variable "postgres_host" {
}

variable "postgres_prefix" {
  default = "taro-test-server"
}

variable "postgres_port" {
  default = "5432"
}

variable "postgres_user" {
  default = "postgres"
  sensitive = true
}

variable "postgres_password" {
  default = "secret"
  sensitive = true
}

variable "postgres_database" {
  default = "taro-test-db"
}