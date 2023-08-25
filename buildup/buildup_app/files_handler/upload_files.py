import os
import uuid
from django.http import HttpRequest
from google.cloud import storage
from google.oauth2 import service_account


# Used for uploading files to Google cloud.
# Used on the create functions at company_file\views and building_permit_file\views.
def upload(request: HttpRequest , folder: str):
    bucket_name = 'buildup'
    file_stream = request.FILES['link'].file
    _, ext = os.path.splitext(request.FILES['link'].name)

    object_name = f"{folder}/{uuid.uuid4()}{ext}"

    credentials = service_account.Credentials.from_service_account_file(
        r"")
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_file(file_stream)
    return blob # Returning the blob for using the blob.public_url as the link of the file,
                # on saving the file on database.
