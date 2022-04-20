import urllib.request as dl

import config
import timer


class DownloaderWrapper:

    def __init__(self, resource_url: str, dest: str):
        self.resource_url = resource_url
        self.dest = dest

    @timer.exit_after(config.duration)
    def download(self):
        dl.urlretrieve(self.resource_url, self.dest)

    @timer.exit_after(config.duration)
    def download_pc(self):
        openner = dl.build_opener()
        openner.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36')]
        dl.install_opener(openner)
        dl.urlretrieve(self.resource_url, self.dest)
