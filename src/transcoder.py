from ffmpy import FFmpeg


class TranscoderWrapper:

    def __init__(self, source_dir: str, dest_dir: str):
        self.source = source_dir
        self.dest = dest_dir

    def transcode(self):
        ff = FFmpeg(
            inputs={self.source: None},
            outputs={self.dest: '-c copy -copyts'}
        )
        ff.run()
