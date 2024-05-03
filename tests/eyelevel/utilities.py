import glob
import os
import json
from pprint import pprint
from groundx import Groundx, ApiException
from dotenv import load_dotenv


def list_files(directory, pattern='*'):

    """
    Lists files in the specified directory that match the pattern.

    :param directory: Directory to search in.
    :param pattern: Pattern to match filenames. Default is '*' (all files).
    :return: List of matching filenames.
     Example usage
        files = list_files('/workspaces/vsc-docker-github/tests/eyelevel', '*.*')
        print(files)
    """
    # Construct the full pattern
    search_pattern = os.path.join(directory, pattern)
    
    # Use glob to find all files matching the pattern
    files = glob.glob(search_pattern)
    
    # Extract only the filenames from the full paths
    filenames = [os.path.basename(file) for file in files]
    
    return filenames

def get_bucket(groundx, name):
    response = groundx.buckets.list()

    try:
        d={}
        for bucket in response.body['buckets']:
            # print(bucket['bucketId'], bucket['name'])
            d[bucket['name']]=bucket['bucketId']

    except ApiException as e:
        print(e)
    
    try:
        return d[name]
    
    except KeyError as k:
        return None
    
def create_bucket(groundx, name):

        try:
            response =  groundx.buckets.create(name=name)
            bucket_id = response.body['bucket']['bucketId']
            print("Create bucket Response:", response, "\n\n\n")
            return bucket_id
    
        except ApiException as e:
            print(e)
            return None







# Example usage
files = list_files('/workspaces/vsc-docker-github/tests/eyelevel', '*.*')
print(files)
