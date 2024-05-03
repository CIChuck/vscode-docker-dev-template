import os
import json
from pprint import pprint
from groundx import Groundx, ApiException
from dotenv import load_dotenv
from utilities import list_files, get_bucket, create_bucket
from time import sleep

load_dotenv()
EYE_LEVEL_API_KEY = os.getenv('EYE_LEVEL_API_KEY')

groundx = Groundx(
    #api_key='08011f65-3be8-4c90-8edb-e7921febea7c'
    api_key=EYE_LEVEL_API_KEY,

)

bname = "medicare_corpus"
bn = get_bucket(groundx, bname)

if not bn:
    id2 = create_bucket(groundx, bname)
    print("Bucket Fetched:", id2)
else:
    id2 = bn
    print("bucket name exists")

source_dir = "/workspaces/vsc-docker-github/tests/eyelevel/corpus/Medicare corpus/"

targets = list_files(source_dir, '*.pdf')
print(targets)
index = 0

if id2:
    
    for fname in targets:
        
        print(f"ingesting: {fname}\n")
        response = groundx.documents.upload_local([{
            "blob": open(source_dir+fname, "rb"),
            "metadata": {
                "bucketId": id2,
                #"fileName": "corpus/Clm104c-01.pdf",
                "fileName": fname,
                "fileType": "pdf"
            }
        }])
        print(f"Completed: {fname}\n\n")
        index += 1

        if index % 32 == 0:
            sleep(60)



