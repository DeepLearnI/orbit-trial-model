import os
from google.cloud import storage
import pandas as pd
from constants import bucket_name

def _check_if_dir_exist(folder):
    import os
    if not os.path.exists(folder):
        os.makedirs(folder)

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    _check_if_dir_exist('data')
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
    download_blob(bucket_name, filename, filepath)
    df = pd.read_csv(filepath)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df


def save(key, df):
    filename = "{}.csv".format(key)
    filepath = os.path.join("data", filename)
    df.to_csv(filepath, index=False)
    upload_blob(bucket_name, filepath, filename)