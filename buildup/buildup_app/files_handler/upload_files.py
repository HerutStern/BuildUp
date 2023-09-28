import os
import uuid
from django.http import HttpRequest
from google.cloud import storage
from google.oauth2 import service_account


# Used for uploading files to Google cloud.
# Used on the create functions at company_file\views and building_permit_file\views.
def upload(request: HttpRequest , folder: str):
    # Defining the name of the Google Cloud Storage bucket
    bucket_name = 'buildup'

    # Retrieving the uploaded file and extract its file stream and extension
    file_stream = request.FILES['link'].file
    _, ext = os.path.splitext(request.FILES['link'].name)

    # Creating a unique object name for the file within the storage bucket
    object_name = f"{folder}/{uuid.uuid4()}{ext}"

    # Authenticating and establishing a connection to Google Cloud Storage
    # credentials = service_account.Credentials.from_service_account_file(
    #     r"C:\BuildUp\buildup-395918-6367d8cbaea8.json")
    credentials = service_account.Credentials.from_service_account_file(
        "buildup/buildup_app/files_handler/buildup-395918-6367d8cbaea8.json")
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)

    # Creating a blob and upload the file's content to it
    blob = bucket.blob(object_name)
    blob.upload_from_file(file_stream)


    return blob # Returning the blob for using the blob.public_url as the link of the file,
                # when saving the file to the database.
