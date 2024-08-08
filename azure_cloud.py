from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import json

# RETRIVE TOKEN FROM JSON FILE
try:
    with open('azure-token.json', 'r') as file:
        token = json.load(file)
        token = token.get('token')
except:
    token=None


# FUNCTION TO UPLOAD FILES INTO AZURE CLOUD STORAGE AND RETRIEVE PUBLIC URL
def uploadfile_azure(
        file_name: str,
        path_file: str=None,
        url_expiry_hours: int=3,
        account_name: str='clearsafetyfiles',
        container_name: str='temporaryfiles',
        ):
    
    '''
    This function upload a file into a Container, from an Azure Blob Storage account.
    It also creates a SAS (Shared Access Signature) of the blob and returns its public url.
    
    Parameters
        - file_name: str - The name of the file to be uploaded. Ex.: 'file.txt'
        - path_file: str=None - The path where it's found the file to be uploaded. Ex.: 'assets/upload'
        - url_expiry_hours: int=3 - The total of hours that the public URL will be valid.
        - account_name: str='clearsafetyfiles' - The Azure Storage Account name.
        - container_name: str='temporaryfiles' - The container name where the files will be uploaded
    
    Returns: str with the public URL | None
    '''
    
    # CHECK IF THE TOKEN HAS BEEN SUCCESSFULLY LOAD
    if token == None:
        return None

    # CREATE A VARIABLE WITH THE CURRENT DATETIME TO BE ADDED TO THE BLOB_NAME
    try:
        datetime_now = datetime.now().strftime('%d_%m_%Y_%HH%MM%SS')
        blob_name = f'{datetime_now}_{file_name}'
    except:
        return None
    
    # CREATE A BLOB SERVICE TO WORK ON THE CONTAINERS
    try:
        blob_service = BlobServiceClient(
            account_url=f'https://{account_name}.blob.core.windows.net/',
            credential=token
        )
    except:
        return None
    
    # CREATE A BLOB IN A CERTAIN CONTAINER
    try:
        new_blob = blob_service.get_blob_client(
            container=container_name,
            blob=blob_name
        )
    except:
        return None

    # UPLOAD A FILE INTO THE BLOB CREATED IN THE PREVIOUS STEP
    try:
        data = f'{path_file}/{file_name}' if path_file != None else f'{file_name}'
        with open(data, 'rb') as file:
            new_blob.upload_blob(file, overwrite=True)
    except:
        return None    

    
    # GENERATE A SAS TOKEN
    try:
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=token,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now() + timedelta(hours=url_expiry_hours)
        )
    except:
        return None
    
    return {
        'url': f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}",
        'blob_name': blob_name
        }




# FUNCTION TO DELETE FILES FROM  AZURE CLOUD STORAGE
def deletefile_azure(
        blob_name: str,
        account_name: str='clearsafetyfiles',
        container_name: str='temporaryfiles',
        ):
    
    '''
    This function deletes a file (blob) from a Container, from an Azure Blob Storage account.
    
    Parameters
        - blob_name: str - The name of the blob returned from the function 'uploadfile_azure'
        - account_name: str='clearsafetyfiles' - The Azure Storage Account name.
        - container_name: str='temporaryfiles' - The container name where the files will be uploaded
    
    Returns: str with the public URL | None
    '''
    
    # CHECK IF THE TOKEN HAS BEEN SUCCESSFULLY LOAD
    if token == None:
        return None
    
    # CREATE A BLOB SERVICE TO WORK ON THE CONTAINERS
    try:
        blob_service = BlobServiceClient(
            account_url=f'https://{account_name}.blob.core.windows.net/',
            credential=token
        )
    except:
        return None
    
    # SELECT A BLOB FROM A CERTAIN CONTAINER
    try:
        blob = blob_service.get_blob_client(
            container=container_name,
            blob=blob_name
        )
    except:
        return None
    
    blob.delete_blob()
    





if __name__ == '__main__':
    file_name = 'requirements.txt'
    #print(uploadfile_azure('requirements.txt'))
    deletefile_azure(file_name)





#pip install azure-storage-blob
#Get the credential from Security + networking / Access keys
#Doc about API https://learn.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme?view=azure-python
                #https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobclient?view=azure-python
# https://pypi.org/project/azure-storage-blob/#description