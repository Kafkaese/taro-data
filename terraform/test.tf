resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = var.resource_group_name
}

resource "azurerm_postgresql_flexible_server" "pg-server" {
  name = var.postgres_server
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku_name = "B_Standard_B1ms"
  storage_mb = 32768
  version = 11
  administrator_login = var.postgres_user
  administrator_password = var.postgres_password
}

resource "azurerm_postgresql_flexible_server_database" "pg-db" {
  name = var.postgres_database
  server_id = azurerm_postgresql_flexible_server.pg-server.id
  charset = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_postgresql_firewall_rule" "pg-server-open" {
  name                = "allpublic"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_flexible_server.pg-server.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}
