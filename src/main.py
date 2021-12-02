import douyu
import idm
import transcode
import datetime


def main():
    room_id = input('Type room id(douyu.com): \n')
    dur = input('Set downloading/recording duration(in sec): \n')
    dur = int(dur)
    idm.timeout = dur
    s = douyu.DouYu(room_id)
    url = s.get_real_url()['flv']
    dest = '../download/'
    filename = \
        dest + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M_') + 'DouYu_'\
        + \
        str(room_id)
    filename_before = filename + '.flv'
    filename_after = filename + '.mp4'
    dm = idm.download_wrapper(url, filename_before)
    try:
        print('Start downloading/recording... Duration set to: ' + str(
            idm.timeout) + 's')
        dm.download()
    except KeyboardInterrupt:
        print('Download Completed')
        me = transcode.transcode_wrapper(filename_before, filename_after)
        me.transcode()
        print('Filename after transcode: ' + filename_after)


if __name__ == '__main__':
    main()