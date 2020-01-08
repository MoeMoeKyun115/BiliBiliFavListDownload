import json
from BiliDown import BiliDownloader
from Database import Postgresql

if __name__ == '__main__':
    config_file = open('config.json', 'r')
    config = json.load(config_file)
    cookie = config['cookie']
    pg_conf = config['pg_config']

    pg = Postgresql(pg_conf)
    bilidown = BiliDownloader(cookie, pg)
    

    flist_id = config['flist_id']
    flist = bilidown.get_flist_list_from_bilibili(flist_id)

    db_flist = pg.get_db_flist()
    flist = list(set(flist) - set(db_flist))

    if len(flist) == 0:
        print('Not new video(s) added to flist')
    else:
        pg.insert_flist(flist, flist_id)
    
    download_list = pg.get_db_flist(condition='WHERE download = false')
    if len(download_list) == 0:
        print('Not new video(s) need to download')
    else:
        bilidown.download(download_list)

