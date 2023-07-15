variable "resource_group_location" {
  default     = "germanywestcentral"
  description = "Location of the resource group."
}

variable "resource_group_name" {
  default     = "taro-test-env"
  description = "The resource group name."
}

variable "image_registry_credential_user" {
  default = "user"
}

variable "image_registry_credential_password" {
  default = "secret"
}