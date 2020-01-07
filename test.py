import BiliUtil
import requests
import json
from Database import Postgresql

def get_flist_list_from_bilibili(flist_id):
    page = 1
    media_list = []
    while True:
        print(f'search flist {flist_id} page {page}')
        flist_url = f'https://api.bilibili.com/medialist/gateway/base/spaceDetail?media_id={flist_id}&pn={page}&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
        r = requests.get(flist_url)
        res = r.json()
        media_count = res['data']['info']['media_count']
        # print(f'count:{media_count}')
        if media_count < 1:
            break
        for media in res['data']['medias']:
            media_list.append(media['id'])
        page += 1
    
    # return {'fid':flist_id, 'medias':media_list}
    return media_list

def download_videos(pg, cookie, download_list):
    print(f'download list size: {len(download_list)}')
    for avid in download_list:
        album = BiliUtil.Album(avid)
        album_info = album.sync(cookie)
        print(album.name)
        video_list = album.get_video_list()
        for video in video_list:
            video.sync(cookie)
            print(f'height:{video.height}, width:{video.width}, quality:{video.quality}')
            task = BiliUtil.Task(video, f"download/{album.aid}", f'{video.name}')
            task.start()
            pg.update_download_status(avid, True)

if __name__ == '__main__':
    config_file = open('config.json', 'r')
    config = json.load(config_file)
    cookie = config['cookie']
    pg = Postgresql(config['pg_config'])

    flist_id = config['flist_id']
    flist = get_flist_list_from_bilibili(flist_id)

    db_flist = pg.get_db_flist()
    flist = list(set(flist) - set(db_flist))

    if len(flist) > 0:
        pg.insert_flist(flist, flist_id)
    else:
        print('Not new video(s) added to flist')

    # download_list = pg.get_db_flist(condition='WHERE download = false')
    # download_videos(pg, cookie, download_list)