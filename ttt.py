# Imports the Google Cloud client library
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.bucket('snarc-dataset')
blob = bucket.blob('filename11.csv')
blob.upload_from_string('uploaded/uploaded/upload_test.csv')
print('Uploaded to GCS')

