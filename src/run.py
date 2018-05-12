import refresher
import utils.cron as cron

def loop():
    
    data = refresher.read_data_from_json

    new_shape_file = refresher.request_new_shapefiles(data)

    if new_shape_file:
        cron.job_in_days(30)
    else:
        cron.job_in_days(2)

if __name__ == "__main__":
    loop()