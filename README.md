# bilibiliDownloadVideo

![python](https://img.shields.io/badge/python-3.7.2-blue.svg)  ![platform](https://img.shields.io/badge/platform-win--32%20%7C%20win--64-blue.svg)

不登录的情况下，下载B站的普通视频（自动选择能下载的最高清晰度，不包括大会员专用清晰度）和弹幕（可选）

# Notice
仅用于学习交流，请勿用于任何商业用途！谢谢!

# Prerequisites
下载并安装[ffmpeg](http://www.ffmpeg.org/download.html)，然后[添加到系统环境变量](https://blog.csdn.net/Chanssl/article/details/83050959)
```
>=python 3.7
pip3 install -r requirements.txt
```

# Usage
```
python Bilibili.py -i (B站普通视频的AV号，不要加av前缀) 
                   -d (可选，下载目录，默认为文件所在路径的video文件夹下) 
                   -D (可选，是否下载弹幕，填写一个非0值表示下载弹幕，下载到和视频放在一起)
```

# License
![MIT](https://img.shields.io/github/license/MarcWarrior/bilibiliDownloadVideo.svg?style=flat)
