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
from utils.ipam_slack_notifier import SlackBOT
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
            print 'oi'
            mdl.drop_table()

        call(
            TERMINAL_COMMAND.format(EXTRACTED_SHAPEFILES_PATH_FOLDER,
                                    shp_file_name, TABLE_NAME),
            shell=True)

        write_data_on_json(
            {
                'ano': ano,
                'mes': mes,
                'url': url
            })

        mdl.database_calculate_and_drop_table()

        print url.format(str(ano), str(zeroFill_mes if zeroFill_mes else mes))

        return True
    return False


try:
    data = read_data_from_json()
    is_new_shapefiles_generated = request_new_shapefiles(data)
    
    if (is_new_shapefiles_generated):
        SlackBOT().send_msg(
            '[+] Imazon shapefile atualizado :+1: ',
            '#imazongeo')
    else:
        SlackBOT().send_msg('[-] Imazon shapefile NAO atualizado :+1: ', '#imazongeo')

except:
    SlackBOT().send_msg('[-] Ocorreu algum erro :-1: ', '#imazongeo')

