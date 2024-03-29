# Resource group shared by all resources in staging environment
resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = var.resource_group_name
}

# Container regsitry for all containers in the staging environemtn (api, frontend and pipeline)
resource "azurerm_container_registry" "container-registry" {
  name                = var.container_registry_name
  
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
}
/*
# Container Instance for the frontend
resource "azurerm_container_group" "container-instance" {
  name                = var.instance_name
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  ip_address_type     = "Public"
  os_type             = "Linux"

  image_registry_credential {
    username = var.image_registry_credential_user
    password = var.image_registry_credential_password
    server   = azurerm_container_registry.container-registry.login_server
  }

  container {
    name   = "taro-frontend"
    image  = "${var.image_registry_login_server}/taro:frontend"
    cpu    = "0.5"
    memory = "1.5"
    environment_variables = {
      ENV=var.environment
    }

    ports {
      port     = 3000
      protocol = "TCP"
    }
  }

  tags = {
    environment = var.environment
  }
}
*/
# Container Instance for the api
resource "azurerm_container_group" "container-instance-api" {
  name                = var.instance_name_api
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  ip_address_type     = "Public"
  os_type             = "Linux"

  image_registry_credential {
    username = var.image_registry_credential_user
    password = var.image_registry_credential_password
    server   = azurerm_container_registry.container-registry.login_server
  }

  container {
    name   = "taro-api"
    image  = "${var.image_registry_login_server}/taro:api"
    cpu    = "0.5"
    memory = "1.5"
    environment_variables = {
      ENV=var.environment
    }

    ports {
      port     = 8000
      protocol = "TCP"
    }
  }

  tags = {
    environment = var.environment
  }
}

# Random id for pg server
resource "random_id" "pg-server-id" {
    byte_length = 8
    prefix = "taro-staging-server"
} 

# Postgres server
resource "azurerm_postgresql_flexible_server" "pg-server" {
  name = "${lower(random_id.pg-server-id.hex)}"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku_name = "B_Standard_B1ms"
  storage_mb = 32768
  version = 11
  administrator_login = var.postgres_user
  administrator_password = var.postgres_password
  zone = 2
}

# Database on postgres server
resource "azurerm_postgresql_flexible_server_database" "pg-db" {
  name = var.postgres_database
  server_id = azurerm_postgresql_flexible_server.pg-server.id
  charset = "UTF8"
  collation = "en_US.utf8"
}

# Firewall rule for the postgres server !!! currently open to all IP addresses
resource "azurerm_postgresql_flexible_server_firewall_rule" "pg-server-open" {
  name                = "allpublic"
  server_id           = azurerm_postgresql_flexible_server.pg-server.id
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}

