from google.cloud import storage


class BucketManager:
    def __init__(self, bucket_name):
        # Use the provided bucket name or default to environment variable
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def list_blob_names_with_suffix(self, suffix):
        """
        Lists all blob names in the bucket with the specified suffix.
        
        :param suffix: The suffix to filter blobs by.
        :return: List of blob names with the specified suffix.
        """
        blobs = self.storage_client.list_blobs(self.bucket_name)
        filtered_blobs = [blob.name for blob in blobs if blob.name.endswith(suffix)]
        return filtered_blobs

    def read_blob(self, path):
        """
        Reads a blob from the bucket at the specified path.
        
        :param path: The path to the blob in the bucket.
        :return: Blob object.
        """
        blob = self.bucket.blob(path)
        return blob

    def get_files_with_prefix(self, prefix):
        """
        Gets all file names in the bucket that start with the specified prefix.
        
        :param prefix: The prefix to filter blobs by.
        :return: List of file names with the specified prefix.
        """
        print(f'prefix is: {prefix}')
        blobs = self.storage_client.list_blobs(self.bucket_name, prefix=prefix)
        file_names = [blob.name for blob in blobs]
        return file_names
    
    def upload_file(self, file_obj, blob_name, content_type="application/octet-stream"):
        """
        Uploads a file to the Google Cloud Storage bucket with the specified blob name.

        :param file_obj: File-like object to upload (e.g., open file in binary mode or BytesIO).
        :param blob_name: The name to use for the blob in the bucket.
        :param content_type: MIME type of the file. Defaults to 'application/octet-stream'.
        """
        blob = self.bucket.blob(blob_name)
        blob.upload_from_file(file_obj, content_type=content_type)
        print(f"File uploaded to bucket '{self.bucket.name}' as '{blob_name}'.")
