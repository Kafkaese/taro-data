output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "server_name" {
  value = azurerm_postgresql_flexible_server.pg-server.name
}