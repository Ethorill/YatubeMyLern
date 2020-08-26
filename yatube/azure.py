from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = 'djangosorega'
    account_key = '7fPEP/iLI8p6Miq4e6YcXZmMTpvENSwtUVkNbM4s2LaovLnZWz4nvqZkDUVJNKmf3GMWl/VcM3ZRSbN6hy7rzw=='
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = 'djangosorega'
    account_key = '7fPEP/iLI8p6Miq4e6YcXZmMTpvENSwtUVkNbM4s2LaovLnZWz4nvqZkDUVJNKmf3GMWl/VcM3ZRSbN6hy7rzw=='
    azure_container = 'static'
    expiration_secs = None