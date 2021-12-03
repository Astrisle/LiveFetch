import urllib.request as dl

import timer
import config


class DownloaderWrapper:

    def __init__(self, resource_url: str, dest: str):
        self.resource_url = resource_url
        self.dest = dest

    @timer.exit_after(config.duration)
    def download(self):
        dl.urlretrieve(self.resource_url, self.dest)
