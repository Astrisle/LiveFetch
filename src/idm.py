import comtypes.client as cc
import comtypes
import logging
import timer
import urllib.request as dl
import multiprocessing
import time


@timer.exit_after(10)
def download_test(url: str):
    dl.urlretrieve(url, '../download/test.flv')


if __name__ == '__main__':
    url = 'http://dyscdnali1.douyucdn.cn/live/288016rlols5.flv?uuid='
    download_test(url)
