import BiliUtil
import requests
import threading
import queue
from Thread import Worker

class BiliDownloader:

    def __init__(self, cookie, pg):
        self.cookie = cookie
        self.pg = pg

    def get_flist_list_from_bilibili(self, flist_id):
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

    def down_album(self, aid, num):
        album = BiliUtil.Album(aid)
        album.sync(self.cookie)
        video_list = album.get_video_list()
        for video in video_list:
            video.sync(self.cookie)
            print(f'''
                **********************************************************************
                Worker {num} is downloading av{aid}...\n
                Height:{video.height}, Width:{video.width}, Quality:{video.quality}\n
                **********************************************************************\n
                ''')
            task = BiliUtil.Task(video, f"download/{album.aid}", f'{video.name}')
            task.start()
            self.pg.update_download_status(album.aid, True)

    def download(self, download_list):
        print(f'download list size: {len(download_list)}')
        album_queue = queue.Queue()
        for aid in download_list:
            # self.down_album(aid)
            album_queue.put(aid)
        
        lock = threading.Lock()

        worker1 = Worker(album_queue, 1, lock, self.down_album)
        worker2 = Worker(album_queue, 2, lock, self.down_album)
        worker3 = Worker(album_queue, 3, lock, self.down_album)

        worker1.start()
        worker2.start()
        worker3.start()

        worker1.join()
        worker2.join()
        worker3.join()

        print('done')


