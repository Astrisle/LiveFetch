from ffmpy import FFmpeg

import config


class FFDownloaderWrapper:
    def __init__(self, url: str, dest: str):
        self.url = url
        self.dest = dest

    def download(self):
        ff = FFmpeg(global_options={'-hide_banner -loglevel warning'},
                    inputs={self.url: ['-t', str(config.duration)]},
                    outputs={self.dest: [
                        '-user_agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                        '-c',
                        'copy',
                        '-f',
                        'mp4',
                        '-movflags',
                        'frag_keyframe',
                        '-min_frag_duration',
                        '60000000'
                    ]})
        ff.run()
