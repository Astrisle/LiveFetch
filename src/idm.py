import comtypes.client as cc
import comtypes
import logging
import timer
import urllib.request as dl
import multiprocessing
import time


class download_wrapper:

    def __init__(self, dl_timeout: int, resource_url: str, dest: str):
        self.resource_url = resource_url
        self.dest = dest
        self.timeout = dl_timeout

    @timer.exit_after()
    def download(self):
        dl.urlretrieve(self.resource_url, self.dest)
