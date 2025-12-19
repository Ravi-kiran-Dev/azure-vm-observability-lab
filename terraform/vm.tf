resource "azurerm_linux_virtual_machine" "vm" {
  name                = "vm-monitoring-lab"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_Ds1_v2"
  admin_username      = "azureuser"
  admin_password      = "Password@123!" # temp, improve later
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.nic.id
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  tags = azurerm_resource_group.rg.tags
}
