variable "resource_group_location" {
  default     = "germanywestcentral"
  description = "Location of the resource group."
}

variable "resource_group_name" {
  default     = "taro-test-env"
  description = "The resource group name."
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