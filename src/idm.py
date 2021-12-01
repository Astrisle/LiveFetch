import comtypes.client as cc
import comtypes
import logging
import urllib.request as dl
import multiprocessing
import time


def tick_tok(target: int):
    for i in range(target):
        print('time elapsed: ' + str(i) + 'sec')
        time.sleep(1)


def download_test(url: str):
    dl.urlretrieve(url, './download/test.flv')


if __name__ == '__main__':
    url = 'http://dyscdnali1.douyucdn.cn/live/288016rlols5.flv?uuid='
    p = multiprocessing.Process(target=download_test(url))
    p.start()
    time.sleep(15)
    p.terminate()
    print('Download Process Terminated')
