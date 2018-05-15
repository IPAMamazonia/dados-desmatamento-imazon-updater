import refresher


def loop():
    
    data = refresher.read_data_from_json()

    is_new_shapefiles = refresher.request_new_shapefiles(data)

if __name__ == "__main__":
    loop()