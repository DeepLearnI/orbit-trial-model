import os
from google.cloud import storage
import pandas as pd

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print('Blob {} downloaded to {}.'.format(source_blob_name, destination_file_name))

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))

def load(key):
    filename = "{}.csv".format(key)
    filepath = os.path.join("data", filename)
    download_blob('orbit-trial', filename, filepath)
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    return df

def save(key, df):
    file_name = "{}.csv".format(key)
    file_path = os.path.join("data", file_name)
    df.to_csv(file_path, index=False)
    upload_blob('orbit-trial', file_path, file_name)