terraform {
  required_version = ">=0.12"

  backend "azurerm" {
    resource_group_name  = "taro"
    storage_account_name = "taro"
    container_name       = "terraform-test-env"
    key                  = "test.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
}

provider "azurerm" {
  features {}
}