# resource group for all Azure resources
resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = var.resource_group_name
}

/*
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
*/ 

# Container registry for the API 
resource "azurerm_container_registry" "taro-staging-registry" {
  name                = "taroStagingContainerRegistry"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
}
/*
# Azuread application needed to assign service principal to container registry. What does this actullay do???
resource "azuread_application" "taro-registry-app" {
  display_name = "taro-registry-app"
}

# Service principal for the container regsitry
resource "azuread_service_principal" "taro-registry-sp" {
  application_id = "${azuread_application.taro-registry-app.application_id}"
}

# Password for the service principal for container registry
resource "azuread_service_principal_password" "taro-registry-sp-pass" {
  service_principal_id = "${azuread_service_principal.taro-registry-sp.id}"
}

# Role assignement service principal to container registry
resource "azurerm_role_assignment" "taro-registry-assignment" {
  scope                = "${azurerm_container_registry.taro-registry.id}"
  role_definition_name = "Administrator"
  principal_id         = "${azuread_service_principal_password.taro-registry-sp-pass.service_principal_id}"
}

# login?
output "docker" {
  value = "docker login ${azurerm_container_registry.taro-registry.login_server} -u ${azuread_service_principal.taro-registry-sp.application_id} -p ${azuread_service_principal_password.taro-registry-sp-pass.value}"
  sensitive = true
}
*/