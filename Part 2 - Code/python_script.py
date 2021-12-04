################################################################################################################
######                                    IMPORT PACKAGES                                               ########
################################################################################################################

import numpy as np
from numpy import genfromtxt
import os
import json
import time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

################################################################################################################
######                                    GLOBAL VARIABLES                                              ########
################################################################################################################

# Access point to Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING="<STRING-CONNECTION>
name_container = "<CONTAINER>"

################################################################################################################
######                                           FUNCTIONS                                              ########
################################################################################################################

# Upload files in Azure
def upload_file(blob_service_client, container_name, blob_name, upload_file_path):
    try:
        print("\nUploading to Azure Storage as blob:\n\t" + blob_name)
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
    except Exception as e:
        # If container exists just use it
        if(type(e).__name__ == "ResourceExistsError"):
            print ("File already exists. Deleting previous version...")
            # Upload the created file
            with open(upload_file_path, "rb") as data:
                blob_client.delete_blob()
            # Upload the created file
            with open(upload_file_path, "rb") as data:
                blob_client.upload_blob(data)

################################################################################################################
######                                    MAIN FUNCTION                                                 ########
################################################################################################################
    
def main():

    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        # Upload file
        upload_file(blob_service_client, name_container, "data_csv.csv", "./data/data_csv.csv")
        # Wait one mintute
        time.sleep(20)
        # Call docker
        os.system('docker run demo_tsi')

    except Exception as e:
        print('Exception:')
        print (e)

            
################################################################################################################
######                                    RUN MAIN FUNCTION                                             ########
################################################################################################################

main()
