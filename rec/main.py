import backoff

import douyu
import ffdownloader
import config
import datetime
import time
import os

import logging

from sys import exit
from ffmpy import FFRuntimeError

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
                      FFRuntimeError,
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
        url = s.get_real_url()
    logging.info('Current time - ' +
                 datetime.datetime.now().strftime('%H:%M:%S'))
    logging.info('Resolved stream source url: ' + url)
    ffdm = ffdownloader.FFDownloaderWrapper(url, filepath)
    logging.info('File path: ' + filepath)
    logging.info('Start downloading/recording... Duration set to: ' + str(
        config.duration) + 's')
    # Start
    ffdm.download()


def main(use_pc: bool = True):
    # room_id = input('Type room id then press Enter(douyu.com): \n')
    room_id = config.rid

    logging.info('Initialising task sequence...USING: PC'
                 if use_pc else 'Initialising task sequence...USING: Mobile')
    dest = '/Volumes/ext/recordings/'
    filename = \
        dest + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M_') + 'DouYu_' \
        + str(room_id) + '.mp4'
    try:
        resolve_and_download(room_id, filename, use_pc)
    except FFRuntimeError:
        logging.warning(
            'Max retires exceeded, resolved source url not reachable, '
            'changing platform...'
        )
        main(not use_pc)
        exit()

    logging.info('Download sequence completed without issue.')
    if config.auto_shutdown:
        logging.warning(
            'SHUTTING DOWN IN 15 SECONDS PER SETTING, PRESS CTRL-C TO CANCEL')
        time.sleep(15)
        os.system('shutdown -s')
    else:
        pass


if __name__ == '__main__':
    # TODO - Take command line argument to dictate use PC or mobile api
    # parser = argparse.ArgumentParser(description='DouYu Streaming Recorder')
    # parser.add_argument('-p', '--use_pc', action='store_true')
    main(config.use_pc)
