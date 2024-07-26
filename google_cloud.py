# INSTALL pip install --upgrade google-cloud-storage

import os
from google.cloud import storage
from google.api_core.exceptions import NotFound
import datetime


try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='public-url-for-airtalbe-1632939c17f2.json'
    credential_setup = True
except:
    credential_setup = False


# Function to upload file into Google Cloud Storage, turn it public and get its URL.
# For this function, it's mandatory to have the file path
def upload_to_googlecloud(file_name, file_path, bucket_name='files_to_airtable'):
    if credential_setup:
        try:
            # Instantiates the storage client
            storage_client = storage.Client()
            
            # Bucket and blob references
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(file_name)
            
            # Uplod
            blob.upload_from_filename(file_path)
            
            # Make it public
            blob.make_public()
            
            # Get URL
            public_url = blob.public_url
            
            return public_url
        
        except Exception as e:
            return False
    
    else:
        return False

#https://www.youtube.com/watch?v=pEbL_TT9cHg




# Function to create a SIGNED_URL to upload files into Google Cloud Storage
def generate_upload_signed_url_v4(file_name, bucket_name='files_to_airtable'):
    """Generates a v4 signed URL for uploading a blob using HTTP PUT.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    https://cloud.google.com/storage/docs/samples/storage-generate-upload-signed-url-v4#storage_generate_upload_signed_url_v4-python
    """
    
    if credential_setup:
        
        try:
            # Instantiates the storage client
            storage_client = storage.Client()
            
            # Bucket and blob references
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)

            url = blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(minutes=60), # This URL is valid for X minutes
                method="PUT", # Allow PUT requests using this URL.
                # content_type="application/octet-stream",  #Valid for all file types
                # headers={'Content-Type': 'application/octet-stream'}
            )

            return url
    
        except:
            return False
    
    else:
        return False




# Function to make a file from the Google Cloud Storage public and to get its URL
# I used it in the situation that the upload into Google is carried out using signed URL instead of file path
def make_file_public_and_get_url(file_name, bucket_name='files_to_airtable'):
    if credential_setup:
        
        # Instantiates the storage client
        storage_client = storage.Client()

        # Bucket and blob references
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        try:
            # Make it public
            blob.make_public()

            # Get the URL
            public_url = blob.public_url

            return public_url
        
        except:
            return False

    else:
        return False


if __name__ == '__main__':
    ...