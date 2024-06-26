import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment

# 设置目标网站的URL
url = 'https://lu-sycdn.kuwo.cn/4d0e213c2c8f916202a6002d7c02e93c/65376c1f/resource/n1/55/12/1098155463.mp3?bitrate$128&format$mp3&type$convert_url2'

# 发送GET请求以获取网页内容
response = requests.get(url)

# 检查是否成功获取网页内容
if response.status_code == 200:
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找包含音频数据的标签（例如，<audio>标签）
    audio_tag = soup.find('audio')

    if audio_tag:
        # 获取音频文件的URL
        audio_url = audio_tag['src']

        # 发送GET请求以获取音频数据
        audio_response = requests.get(audio_url)

        # 检查是否成功获取音频数据
        if audio_response.status_code == 200:
            # 保存音频数据到本地文件
            with open('audio.mp3', 'wb') as audio_file:
                audio_file.write(audio_response.content)
                print('音频数据已保存为 audio.mp3')
        else:
            print('无法获取音频数据')
    else:
        print('未找到音频标签')
else:
    print('无法获取网页内容')

