import urllib.error

import backoff

import douyu
import downloader
import transcoder
import config
import datetime
import os

import logging

logging.basicConfig(level=logging.INFO)


def resolve_fail_handler(detail):
    logging.warning('Resolve attempts: {tries}'.format(**detail))
    logging.warning('Stream not started or RID not valid, retry in '
                    'around ' +
                    str(config.resolve_retry_timeout) + ' sec...')


def download_fail_handler(detail):
    logging.warning('Download attempts: {tries}'.format(**detail))
    logging.warning('Failed retrieving file from resolved url, restarting '
                    'sequence in around ' + str(config.download_retry_timeout) +
                    ' sec...')


@backoff.on_exception(backoff.constant,
                      urllib.error.HTTPError,
                      jitter=backoff.random_jitter,
                      on_backoff=download_fail_handler,
                      interval=config.download_retry_timeout,
                      max_tries=config.max_retries_for_download,
                      )
@backoff.on_exception(backoff.constant,
                      RuntimeError,
                      jitter=backoff.random_jitter,
                      on_backoff=resolve_fail_handler,
                      interval=config.resolve_retry_timeout
                      )
def resolve_and_download(rid: str, filepath: str, use_pc: bool):
    s = douyu.DouYu(rid)
    if use_pc:
        url = s.get_real_url_pc()
    else:
        url = s.get_real_url()['flv']
    logging.info('Current time - ' +
                 datetime.datetime.now().strftime('%H:%M:%S'))
    logging.info('Resolved stream source url: ' + url)
    dm = downloader.DownloaderWrapper(url, filepath)
    logging.info('File path: ' + filepath)
    logging.info('Start downloading/recording... Duration set to: ' + str(
        config.duration) + 's')
    if use_pc:
        dm.download_pc()
    else:
        dm.download()


def main(use_pc: bool = True):
    # room_id = input('Type room id then press Enter(douyu.com): \n')
    room_id = 520
    processed = False

    logging.info('Initialising task sequence...USING: PC'
                 if use_pc else 'Initialising task sequence...USING: Mobile')
    dest = './recordings/'
    filename = \
        dest + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M_') + 'DouYu_' \
        + str(room_id)
    filename_before = filename + '.flv'
    filename_after = filename + '.mp4'
    try:
        resolve_and_download(room_id, filename_before, use_pc)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            logging.warning(
                'Max retires exceeded, resolved source url not reachable, '
                'changing platform...'
            )
            main(not use_pc)
    except KeyboardInterrupt:
        logging.info('Download sequence terminated... Starting ffmpeg for '
                     'transcode')
        me = transcoder.TranscoderWrapper(filename_before, filename_after)
        me.transcode()
        logging.info('Transcoded file path: ' + filename_after)
        processed = True
        if config.auto_shutdown:
            os.system('shutdown -s')
        else:
            pass

    if processed == False:
        logging.info('Download sequence completed... Starting ffmpeg for '
                     'transcode')
        me = transcoder.TranscoderWrapper(filename_before, filename_after)
        me.transcode()
        logging.info('Transcoded file path: ' + filename_after)
        processed = True
        if config.auto_shutdown:
            os.system('shutdown -s')
        else:
            pass


if __name__ == '__main__':
    main(config.use_pc)
