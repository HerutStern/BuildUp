import os
import uuid
from google.cloud import storage
from google.oauth2 import service_account


def upload(request, folder):
    bucket_name = 'buildup'
    file_stream = request.FILES['link'].file
    _, ext = os.path.splitext(request.FILES['link'].name)

    object_name = f"{folder}/{uuid.uuid4()}{ext}"

    credentials = service_account.Credentials.from_service_account_file(
        r"C:\BuildUp\buildup-395918-6367d8cbaea8.json")
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_file(file_stream)
    return blob
