import json
import re 
import requests as req
import zipfile
from StringIO import StringIO
from file_manager import delete_and_create_folder, extract_zip_to_folder
from json_wr  import *
from subprocess import call


def request_new_shapefiles(data):
    ano = data['ano']
    mes = data['mes']
    url = data['url']

    mes = mes + 1
    zeroFill_mes = None


    if mes > 12:
        mes = 1
        ano = ano + 1
    if mes < 10:
        zeroFill_mes = str(mes).zfill(2)

    resp = req.get(url.format(str(ano), str( zeroFill_mes if zeroFill_mes else mes)), stream=True)

    print url.format(str(ano), str(zeroFill_mes if zeroFill_mes else mes))
    if resp.ok:
        
        delete_and_create_folder()
        extract_zip_to_folder(resp.content)
        
        # call('echo test > tt.txt', shell=True)

        write_data_on_json(
            {
                'ano': ano,
                'mes': mes,
                'url': url
            })
        return True
    return False


data = read_data_from_json()
 


request_new_shapefiles(data)













