from google.cloud import storage
from dotenv import dotenv_values
import os

class GCSClient:
    def __init__(self):
        # Instantiate a client
        config = dotenv_values(".env")
        projectId = config['GC_PROJECT_ID']
        # presumes you have done `gcloud auth login` per https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
        # change projects with 'gcloud config set project GC_PROJECT_ID'
        os.environ.setdefault('GCLOUD_PROJECT', projectId) # not finding it when also using $GOOGLE_APPLICATION_CREDENTIALS = ~/.config/gcloud/legacy_credentials/ryan@deepsearising.com/adc.json
        self.storage_client = storage.Client()
        # presumes bucket already created
        self.bucket_name = config['GCS_BUCKET'] or 'evcharge_data'

    # returns bytes
    def download_blob_into_memory(self, source_blob_name, bucket_name = None):
        # option to override the GCS bucket
        if bucket_name is not(None):
            self.bucket_name = bucket_name

        bucket = self.storage_client.get_bucket(self.bucket_name)
        # The ID of your GCS object
        # source_blob_name = "storage-object-name"
        blob = bucket.blob(source_blob_name)

        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        return blob.download_as_string()
