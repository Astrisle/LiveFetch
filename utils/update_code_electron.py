import ctypes
import os
from pathlib import Path

import requests


def get_gift_codes():
    gift_json = requests.get(
        'https://webconf.douyucdn.cn/resource/common/prop_gift_list'
        '/prop_gift_config.json').text
    return gift_json


def construct_config_file(txt: str, path: str):
    # write data and display stats
    with open(path, 'w', encoding='utf-8') as file:
        file.write(txt)
        ctypes.windll.user32.MessageBoxW(0, "更新成功", '成功', 0)


if __name__ == '__main__':
    dir_path = os.path.realpath(__file__)
    cf_path = Path(dir_path)
    par = cf_path.parent.parent.absolute()
    try:
        construct_config_file(get_gift_codes(), str(par) +
                              '\\resources\\app\\dist\\giftdata.txt')
    except Exception as e:
        if e.__class__.__name__ == 'FileNotFoundError':
            err_str_file = str(par) + ' 没有找到配置文件\n' \
                           '请确保exe文件正确放置在弹幕助手文件夹内 \n' \
                           '如不清楚请参阅使用说明'
            ctypes.windll.user32.MessageBoxW(0, err_str_file,
                                             '未找到配置文件', 0)
        else:
            err_str = str(e) + '\n\n请尽快反馈以上错误信息给开发者'
            ctypes.windll.user32.MessageBoxW(0, err_str, '出现未知异常', 0)
