metadata description = 'Replication of IT Lab 6 core infrastructure using declarative Bicep.'

param location string = 'eastus'
param storageAccountName string = 'cst8921lab6nt123'

// 1. Declare the High-Performance Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
  }
}

// 2. Enable Static Website Hosting natively by the Management Plane
resource staticWebsite 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    staticWebsite: {
      enabled: true
      indexDocument: 'index.html'
      errorDocument404Path: '404.html'
    }
  }
}

output staticWebEndpoint string = storageAccount.properties.primaryEndpoints.web


