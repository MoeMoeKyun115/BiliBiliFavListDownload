import BiliUtil
import requests

class Spider:

    def __init__(self, cookie):
        self.cookie = cookie

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

    def download_videos(self, pg, download_list):
        print(f'download list size: {len(download_list)}')
        for avid in download_list:
            album = BiliUtil.Album(avid)
            album_info = album.sync(self.cookie)
            # print(album.name)
            video_list = album.get_video_list()
            for video in video_list:
                video.sync(self.cookie)
                print(f'height:{video.height}, width:{video.width}, quality:{video.quality}')
                task = BiliUtil.Task(video, f"download/{album.aid}", f'{video.name}')
                task.start()
                pg.update_download_status(avid, True)
