## bilibili视频爬取

## package

```python
import requests
import json
import os
from tqdm import tqdm
```





### 如果想要调整爬取视频的页码

```python
    def Sync_run(self):
        self.num = self._cid_name()
        tn = tqdm(self.cid_list[:10])  # 如果想进行测试, 在这里切片操作只获取前面两个视频即可
```

在 Sync_run中将tqdm()中的cid_list进行切片操作

## RUN

1. 打开想要爬取视频的bilibili网站

2. ```
   比如
   https://www.bilibili.com/video/BV1R7411F7JV?from=search&seid=8624852726982174897&spm_id_from=333.337.0.0
   ```

   - 上述连接中`BV1R7411F7JV`即为 需要在init函数中修改的变量self.avid, 修改该变量即可爬取这个链接目录的所有视频



运行该程序只需要将spyder中初始化的数据, 然后创建对象run即可

## 保存后的视频

保存后的视频如果想要播放需要H.264视频解码器, 经过测试, 只保存videos文件也有音频, 可以通过`potplayer` 播放器，或者其他支持H.264视频解码器的播放器进行播放



