import urllib.request as dl

import timer

timeout = 10


class download_wrapper:

    def __init__(self, resource_url: str, dest: str):
        self.resource_url = resource_url
        self.dest = dest

    @timer.exit_after(timeout)
    def download(self):
        dl.urlretrieve(self.resource_url, self.dest)
