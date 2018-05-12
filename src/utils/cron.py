from crontab import CronTab

import os

my_cron = CronTab(user='filipe')

def job_in_days(days):
    
    job = my_cron.new(command='python /home/filipe/Documentos/shapefiles-updater/refresher.py')
    job.minute.every(3)
    my_cron.write()

def log():
    for d in my_cron.log:
        print d['pid'] + " - " + d['date']