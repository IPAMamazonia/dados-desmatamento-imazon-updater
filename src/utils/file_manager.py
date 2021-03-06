import os
import zipfile
import shutil
import re
from StringIO import StringIO
from file_path_constants import EXTRACTED_SHAPEFILES_PATH_FOLDER

def remove_folder_and_shapeFiles():

    shutil.rmtree(EXTRACTED_SHAPEFILES_PATH_FOLDER)


def delete_and_create_folder():

    if os.path.exists(EXTRACTED_SHAPEFILES_PATH_FOLDER):
        remove_folder_and_shapeFiles()
        os.makedirs(EXTRACTED_SHAPEFILES_PATH_FOLDER)
        
def extract_zip_to_folder(binary_content):
    
    zipfile.ZipFile(StringIO(binary_content)).extractall(
        path=EXTRACTED_SHAPEFILES_PATH_FOLDER)

def generate_file_name(url):

    file_name = re.search('downloads/(.*).zip$', url).group(1)
    file_name = file_name+'.shp'
    return file_name