# from crontab import CronTab

import os

def 
my_cron = CronTab(user='filipe')
job = my_cron.new(command='python /home/filipe/Documentos/shapefiles-updater/refresher.py')
job.minute.every(1)
my_cron.write()
def hel():
    print os.path.abspath(os.path.dirname(__file__))
# with open('/home/filipe/Documentos/shapefiles-updater/testandocron.txt', 'w') as f:
#     f.write('pf1')
#     f.close()
