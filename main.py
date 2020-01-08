import json
from Action import Spider
from Database import Postgresql

if __name__ == '__main__':
    config_file = open('config.json', 'r')
    config = json.load(config_file)
    cookie = config['cookie']
    pg_conf = config['pg_config']

    spider = Spider(cookie)
    pg = Postgresql(pg_conf)

    flist_id = config['flist_id']
    flist = spider.get_flist_list_from_bilibili(flist_id)

    db_flist = pg.get_db_flist()
    flist = list(set(flist) - set(db_flist))

    if len(flist) > 0:
        pg.insert_flist(flist, flist_id)
    else:
        print('Not new video(s) added to flist')

    download_list = pg.get_db_flist(condition='WHERE download = false')
    spider.download_videos(pg, download_list)