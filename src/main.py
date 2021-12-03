import douyu
import downloader
import transcoder
import config
import datetime
import os

import logging

logging.basicConfig(level=logging.INFO)


def main():
    room_id = input('Type room id here(douyu.com): \n')
    # immutable causing trouble
    # dur = input('Set downloading/recording duration(in sec): \n')
    # dur = int(dur)
    # config = __import__('config')
    # config.duration = dur
    logging.info('Initialising task sequence...')
    s = douyu.DouYu(room_id)
    url = s.get_real_url()['flv']
    dest = '../download/'
    logging.info('Resolved stream source url: ' + url)
    filename = \
        dest + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M_') + 'DouYu_' \
        + str(room_id)
    filename_before = filename + '.flv'
    filename_after = filename + '.mp4'
    logging.info('File path: ' + filename_before)
    dm = downloader.DownloaderWrapper(url, filename_before)
    try:
        logging.info('Start downloading/recording... Duration set to: ' + str(
            config.duration) + 's')
        dm.download()
    except KeyboardInterrupt:
        logging.info('Download Completed... Starting ffmpeg for transcode')
        me = transcoder.TranscoderWrapper(filename_before, filename_after)
        me.transcode()
        logging.info('Transcoded file path: ' + filename_after)
        if config.auto_shutdown:
            os.system('shutdown -s')
        else:
            pass


if __name__ == '__main__':
    main()
