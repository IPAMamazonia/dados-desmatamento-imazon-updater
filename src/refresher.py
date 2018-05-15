import json
import re
import requests as req
import zipfile
from StringIO import StringIO
from utils.file_manager import delete_and_create_folder, extract_zip_to_folder, generate_file_name
from utils.json_wr  import *
from subprocess import call
from utils.file_path_constants import EXTRACTED_SHAPEFILES_PATH_FOLDER
from db.configs import *
from db.model import DB_Model

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


    if resp.ok:

        mdl = DB_Model()
        delete_and_create_folder()
        extract_zip_to_folder(resp.content)
        shp_file_name = generate_file_name(url.format( str(ano), str(zeroFill_mes if zeroFill_mes else mes )))

        if mdl.check_if_table_exists():
            mdl.drop_table()

        call(
            TERMINAL_COMMAND.format(EXTRACTED_SHAPEFILES_PATH_FOLDER,
                                    TABLE_NAME, shp_file_name, PW, HOST,
                                    DB_NAME),
            shell=True)

        write_data_on_json(
            {
                'ano': ano,
                'mes': mes,
                'url': url
            })

        mdl.database_calculate_and_drop_table()

        print url.format(str(ano), str(zeroFill_mes if zeroFill_mes else mes))
        print resp.status_code
        return True
    return False
