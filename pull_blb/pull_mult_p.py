
# import ffmpeg
import re
from os import listdir
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from tqdm import tqdm
# from timer import timer
import concurrent.futures   
from ast import literal_eval
from multiprocessing import set_start_method
from os.path import isfile, join
import argparse


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='Az pull description')
parser.add_argument('--file-path', type=str, default = '/mnt/data/files.txt')
parser.add_argument('--cont-cli', type=str, default = 'athenaliveprod')
parser.add_argument('--lang', type=str, default = '')
parser.add_argument('--write-path', type=str, default = '/mnt/data')
args = parser.parse_args()


def pull_main(video_id = None,\
connection_string = "DefaultEndpointsProtocol=https;AccountName=videobank;AccountKey=+7+BZaxs5zBHwyDAMJHnMEJS1mhzIN4AC6PS7wIbVgE1hd35eHEB9IAbc+E2PfV4GNP7dkFrWiLAVMZ8HgnFEw==;EndpointSuffix=core.windows.net", \
container_client = 'athenaliveprod', lang = '', write_path = '/mnt/data'):

    # if isfile(f'../nas_vid/{video_id}.mp4'):
    #     print(f'file already exists')
    #     pass
    # else:
    
    set_start_method("spawn", force=True)
    connect_str = connection_string
    video_id = video_id
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container = blob_service_client.get_container_client(container_client)

    if container_client == 'athenaliveprod':
        blobs = container.list_blobs(name_starts_with=f'athenaliveprod/{video_id}')

    else:
        blobs = container.list_blobs()

    pat_format = re.compile('.*\.mp4')
    pat_lang = re.compile(f'.*{lang}', re.IGNORECASE)
    pat_id = re.compile(f'.*{video_id}', re.IGNORECASE)

    for b in blobs:
        name_blob = b.name
        if re.search(pat_format,name_blob) and re.search(pattern=pat_lang, string=name_blob) and re.search(pattern=pat_id, string=name_blob):
            print('<<<<<    BLOB MATCH FOUND  >>>>')
            print(name_blob)
            print(f"Downloading {video_id}.mp4")
            downloader = container.download_blob(b)
            file_name = name_blob.split('/')[-1]
            with open(f"{write_path}/{video_id}.mp4", 'wb') as f:
                downloader.readinto(f)
            break

file_path = args.file_path
cont_cli = args.cont_cli
lang = args.lang
write_path = args.write_path
print(f'args are >> {str(args)}')

with open(f'{file_path}','r') as file:
    vid_list = literal_eval(file.read())

for video_id in tqdm(vid_list):
    pull_main(video_id =video_id, container_client = cont_cli, lang = lang, write_path = write_path)
    
    
# @timer(1,1)
# def main():
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         executor.map(pull_main, vid_list)
#         executor.shutdown(wait=True)
