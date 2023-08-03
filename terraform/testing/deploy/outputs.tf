output "api-public-ip" {
  value = azurerm_container_group.taro-test-api-instance.ip_address
}