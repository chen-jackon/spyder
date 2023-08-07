import requests
import json
import os
# from tqdm import tqdm
import re


class spyder(object):
    def __init__(self):
        self.bvid = "BV1cu411o7Ym"  # 在打开b站后会获取bvid 具体使用查看readme.md
        self.bvid = input("请输入pvid")
        self.video_list = "https://api.bilibili.com/x/player/pagelist?bvid={}"  # 根据bvid 可以获取当前视频的列表
        end = "bvid={}".format(self.bvid)  # 跟下面的self.video进行拼接, 方便后面的format只对cid进行format
        self.video = "https://api.bilibili.com/x/player/playurl?cid={}&qn=80&type=&otype=json&fourk=1&" + end
        self.headers = {
            'User-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
            'referer': "https://www.bilibili.com/",
        }
        # 指定保存视频的目录
        self.save_file = "../data/"
        # 如果没有保存文件的目录, 新建目录
        if not os.path.exists(self.save_file):
            os.makedirs(self.save_file)

    # 获取视频列表所有视频的cid 和name
    def _cid_name(self):
        res = requests.get(url=self.video_list.format(self.bvid), headers=self.headers).text
        j = json.loads(res)
        n = len(j['data'])
        cid_dir = [cid for cid in j['data']]
        self.cid_list = [cid['cid'] for cid in cid_dir]
        self.name_list = [cid['part'] for cid in cid_dir]
        return n

    # 解析单个cid 对应的视频中的video和 voice， 以及视频质量
    def _parse_cid(self, cid: str):
        u_json = self.video.format(cid)
        res = requests.get(url=u_json, headers=self.headers).text
        j = json.loads(res)
        l = j['data']['durl'][0]['backup_url']
        quality = {}
        quality['accept_description'] = j['data']['accept_description'][0]  # 默认视频质量为最高
        quality['accept_quality'] = j['data']['accept_quality'][0]  # 默认视频质量为最高
        video = str(l[0])
        voice = str(l[1])
        return video, voice, quality

    def Sync_run(self):
        
        self.num = self._cid_name()
        # tn = tqdm(self.cid_list)  # 如果想进行测试, 在这里切片操作只获取前面两个视频即可
        all = []
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # 非法路径名称
        for i, data in enumerate(self.cid_list):
            dic = {}
            dic['name'] = self.name_list[i]  # Video name
            dic['cid'] = self.cid_list[i]  # Video cid
            dic['video'] = self._parse_cid(str(self.cid_list[i]))[0]  # video link
            dic['voice'] = self._parse_cid(str(self.cid_list[i]))[1]  # voice link
            dic['vq'] = self._parse_cid(str(self.cid_list[i]))[2]  # video quality
            all.append(dic)
            print("\n正在保存第{}个视频\n".format(i + 1))
            if os.path.exists(os.path.join(self.save_file, re.sub(rstr, "_", all[i]['name'])) + '.mp4'):
                print(all[i]['name'] + "文件已存在")
                continue
            video_res = requests.get(all[i]['video'], headers=self.headers, params=all[i]['vq'])
            # voice_res = requests.get(self.all[i]['voice'], headers=self.headers)
            # print(self.save_file + self.all[i]['name']+'.mp4')

            with open(os.path.join(self.save_file, re.sub(rstr, "_", all[i]['name'])) + '.mp4', 'wb+')as f:
                f.write(video_res.content)


spyder().Sync_run()
