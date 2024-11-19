from io import BytesIO

from google.cloud import storage

import cv2
import numpy as np
from PIL import Image


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

    def read_image(self,file_name):
        """
        Reads an image file from the specified Google Cloud Storage bucket and converts it into an OpenCV image format.

        :param file_name: The name (or path) of the file within the bucket.
        :return: The image as a NumPy array in OpenCV format (BGR).
        
        Steps:
        - Retrieves the specified blob from the bucket.
        - Downloads the blob content as bytes.
        - Converts the byte data to a NumPy array.
        - Decodes the NumPy array to an image using OpenCV.

        Usage:
        Call this function with the file name of the image you wish to read from the bucket. 
        This function assumes the file is an image and will return it in OpenCV format for further processing.
        """
        blob = self.bucket.blob(file_name)

        # Download image as bytes
        image_bytes = blob.download_as_string()
        
        # Convert bytes to a numpy array
        image_array = np.frombuffer(image_bytes, np.uint8)
        
        # Decode the numpy array as an image
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
    
    def upload_image(self, array, blob_name):
        """
        Uploads an image file to the bucket with the specified blob name.
        
        :param file: The file object to upload.
        :param blob_name: The name for the blob in the bucket.
        """
        image = Image.fromarray(array)
        image_io = BytesIO()
        image.save(image_io, format="PNG")
        image_io.seek(0)
        blob = self.bucket.blob(blob_name)
        blob.upload_from_file(image_io, content_type="image/png")
        print(f"Image uploaded to bucket '{self.bucket_name}' as '{blob_name}'.")

    def upload_file_data(self, file_data, blob_name, content_type):
        """
        Uploads any file to the bucket with the specified blob name and content type.
        :param file_data: The file content as bytes or a file-like object.
        :param blob_name: The name for the blob in the bucket.
        :param content_type: The MIME type of the file (e.g., 'image/png', 'application/json').
        """
        if isinstance(file_data, (bytes, bytearray)):
            file_io = BytesIO(file_data)
        else:
            file_io = file_data  # Assume it's already a file-like object
        file_io.seek(0)  # Ensure the stream is at the start
        blob = self.bucket.blob(blob_name)
        blob.upload_from_file(file_io, content_type=content_type)
        print(f"File uploaded to bucket '{self.bucket_name}' as '{blob_name}' with content type '{content_type}'.")
        
    def upload_blob_from_filename(self, source_file_name, blob_name):
        """Uploads a file to the bucket."""
        blob = self.bucket.blob(blob_name)
        blob.upload_from_filename(source_file_name)
        print(f'{source_file_name} uploaded to {self.bucket_name} as {blob_name}')