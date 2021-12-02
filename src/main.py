import douyu
import idm
import transcode
import datetime


def main():
    room_id = input('Type room id(douyu.com): \n')
    s = douyu.DouYu(room_id)
    url = s.get_real_url()['flv']
    dest = '../download/'
    filename = \
        dest + datetime.datetime.now().strftime('%Y-%m-%d_%H_') + 'DouYu_' + \
        str(room_id)
    filename_before = filename + '.flv'
    filename_after = filename + '.mp4'
    dm = idm.download_wrapper(url, filename_before)
    try:
        dm.download()
    except KeyboardInterrupt:
        print('Download Completed')
        me = transcode.transcode_wrapper(filename_before, filename_after)
        me.transcode()


if __name__ == '__main__':
    main()
