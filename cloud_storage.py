from google.cloud import storage
from threading import Lock

class SingletonGCS:
    _instance = None
    _lock = Lock()

    def __init__(self, project_id):
        if not SingletonGCS._instance:
            with SingletonGCS._lock:
                if not SingletonGCS._instance:
                    SingletonGCS._instance = storage.Client(project=project_id)

    @staticmethod
    def get_instance(project_id):
        if not SingletonGCS._instance:
            SingletonGCS(project_id)
        return SingletonGCS._instance
    
    @classmethod
    def write_to_gcs(cls, gcs_client, bucket_name, key, data):
        # Get the bucket
        bucket = gcs_client.get_bucket(bucket_name)
        # Create a new blob and upload the file
        blob = bucket.blob(key)
        blob.upload_from_string(data)
    
    @classmethod
    def get_from_gcs(cls, gcs_client, bucket_name, key):
    # Get the bucket
        bucket = gcs_client.get_bucket(bucket_name)

        # Get the blob
        blob = bucket.blob(key)

        # Download the blob to a string and return it
        return blob.download_as_text()
