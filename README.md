# LiveFetch


A lightweight project intended for full automation of recording and 
transcode live stream from douyu.com

Based on [real-url](https://github.com/wbt5/real-url) by wbt5.

一个轻量的斗鱼直播流自动下载以及转码脚本

---

## Usage

### Prerequisite

Python 3.9+

[FFmpeg](https://ffmpeg.org/) installed/compiled and added to PATH locally
(Windows)

### How To
1. `cd` to `src`
1. `python main.py`
1. Insert room id, and it will do the rest

### Tips
Should you wish to make any changes, such as save directory for video files, 
FFmpeg cmd args, file names, etc, you`ll need to edit the source code directly

---

## 如何使用

### 前期需求
Python 3.9+

[FFmpeg](https://ffmpeg.org/) 已经于本地完成安装/编译且可执行文件位置添加至Windows系统环境变量

### 实际使用
1. `cd` 至 `src` 目录下
1. `python main.py`
1. 输入房间号, 该脚本会以设定的时间长度自动开始下载指定直播间的视频流并转码

### 提示
如果阁下需要修改配置项目, 如视频文件存储位置, FFmpeg命令行选项, 文件名等, 请直接在源码中找到以上项目进行修改

---

## TODO

- [ ] Code comments(lmao)
- [ ] Bundle all config(filename, directory, etc) to a single file
- [ ] A frontend control panel for further possible functionalities