from google.cloud import storage

class GCloudStorage:
    def __init__(self):
        # Instantiate a client
        self.storage_client = storage.Client()
        # presumes bucket already created
        self.bucket_name = 'evcharge_data'

