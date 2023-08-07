output "api-public-ip" {
  value = azurerm_container_group.api-instance.ip_address
}