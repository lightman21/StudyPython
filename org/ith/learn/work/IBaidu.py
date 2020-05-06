"""
AppID
19733928

API Key
gO5tZ0eDDTptwPyxljTc2cG1

Secret Key
kdEaeG0NmTfjCP3lnKWA1MlIdBgKDlnY

"""
import os
import random
import time

import sys
import time
import requests
import json
import os

from multiprocessing import Process

from aip import AipOcr

from org.ith.learn.util.TUtils import highlight, md5, file_md5, exec_cmd, is_contains_chinese, chunk_in_slice, \
    make_sure_file_exist

APP_ID = '19733928'
API_KEY = 'gO5tZ0eDDTptwPyxljTc2cG1'
SECRET_KEY = 'kdEaeG0NmTfjCP3lnKWA1MlIdBgKDlnY'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# pic_path = '/private/tmp/all_china_53510/res/drawable-hdpi-v4/ic_takeout_order_invalid.png'
# pic_path = '/private/tmp/all_china_53510/res/drawable-hdpi-v4/ic_takeout_order_refund.png'
# pic_path = '/private/tmp/all_china_53510/res/drawable-hdpi-v4/icon.png'
pic_path = '/private/tmp/all_china_53510/res/drawable-hdpi-v4/test.bmp'


def single(path_of_pic):
    with open(path_of_pic, 'rb') as f:
        img = f.read()
        msg = client.basicGeneral(img)
        result = ''
        if msg is not None:
            word_ret = msg.get('words_result')
            if word_ret is not None:
                for i in word_ret:
                    result += i.get('words')
        return result


def do_work():
    dir_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/drawable-xhdpi/'
    dir_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/'

    path_han = list()

    readed_file = set()

    total_pic = 0

    try:
        for dir_path_name, dirs, files in os.walk(dir_path):
            for f in files:
                if len(path_han) > 300:
                    break

                path_of_dir = dir_path_name
                if not dir_path_name.endswith('/'):
                    path_of_dir += os.sep
                full_name = path_of_dir + f
                if full_name.endswith('.png'):
                    total_pic += 1
                    readed_file.add(full_name)
                    ret = single(full_name)
                    print(full_name, ' --> ', highlight(ret, 2))
                    if len(ret) > 0 and is_contains_chinese(ret):
                        line = '{:<100} ---> {:<10} file md5 --> {}\n'.format(full_name, ret,
                                                                              file_md5(full_name))
                        path_han.append(line)
                        every_time = list()
                        every_time.append(line)
                        now_date = time.strftime("%Y_%m_%d_%H:00", time.localtime())

                        with open('./' + now_date + '_work_pic_every_path.xml', 'a+') as rout:
                            rout.writelines(every_time)

    finally:
        with open('./' + md5(dir_path) + '_work_pic_finally_path.xml', 'w') as rout:
            rout.writelines(path_han)
            print('throught all pics ', total_pic)
    pass


def list_item(path_list):

    path_han = list()

    try:
        for full_name in path_list:
            ret = single(full_name)

            time.sleep(random.randint(1, 2))

            print(full_name, ' --> ', highlight(ret, 2))
            if len(ret) > 0 and is_contains_chinese(ret):
                line = '{:<100} ---> {:<10} file md5 --> {}\n'.format(full_name, ret,
                                                                      file_md5(full_name))
                path_han.append(line)
                every_time = list()
                every_time.append(line)
                now_date = time.strftime("%Y_%m_%d_%H:00", time.localtime())

                pic_file = './res/pics/every/' + md5(str(path_list)) + now_date + '_work_pic_every_path.xml'
                make_sure_file_exist(pic_file)

                with open(pic_file, 'a+') as rout:
                    rout.writelines(every_time)

    finally:
        m_file = './res/pics/' + md5(str(path_list)) + '_work_pic_finally_path.xml'
        make_sure_file_exist(m_file)
        with open(m_file, 'w') as rout:
            rout.writelines(path_han)


def loop_pics(pic_list):
    try:
        tproc = Process(target=list_item, args=(pic_list,))
        tproc.start()
    except Exception as e:
        print(e)
        print("Error: 无法启动进程", e)


def main():
    # dir_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/'
    dir_path = '/tmp/wan/'
    all_pics = get_all_pics(dir_path)
    slices = chunk_in_slice(all_pics, 10)
    for item_list in slices:
        loop_pics(item_list)
        print('item_list size ', len(item_list))
    while 1:
        pass

    pass


def get_all_pics(path_of_dir):
    total_pic = list()
    for dir_path_name, dirs, files in os.walk(path_of_dir):
        for f in files:
            path_of_dir = dir_path_name
            if not dir_path_name.endswith('/'):
                path_of_dir += os.sep
            full_name = path_of_dir + f
            if full_name.endswith('.png'):
                total_pic.append(full_name)

    print(highlight('dir_path_name_find_pic', 2), len(total_pic))

    return total_pic


if __name__ == '__main__':
    main()
