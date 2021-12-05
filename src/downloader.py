import urllib.request as dl


class DownloaderWrapper:

    def __init__(self, resource_url: str, dest: str):
        self.resource_url = resource_url
        self.dest = dest

    def download(self):
        dl.urlretrieve(self.resource_url, self.dest)
