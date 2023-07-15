output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
/*
output "acr_service_principal_app_id" {
  value = azurerm_container_registry.taro-registry.identity[0].principal_id
}

output "acr_service_principal_password" {
  value = azurerm_container_registry.taro-registry.identity[0].passwords[0].value
}
*/
#output "server_name" {
#  value = azurerm_postgresql_flexible_server.pg-server.name
#}

output "postgres_server" {
  value = azurerm_postgresql_flexible_server.pg-server.name
}