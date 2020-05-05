"""
AppID
19733928

API Key
gO5tZ0eDDTptwPyxljTc2cG1

Secret Key
kdEaeG0NmTfjCP3lnKWA1MlIdBgKDlnY

"""
import os
import time

from aip import AipOcr

from org.ith.learn.util.TUtils import highlight, md5, file_md5, exec_cmd, is_contains_chinese

APP_ID = '19733928'
API_KEY = 'gO5tZ0eDDTptwPyxljTc2cG1'
SECRET_KEY = 'kdEaeG0NmTfjCP3lnKWA1MlIdBgKDlnY'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# pic_path = '/private/tmp/all_china_53510/res/drawable-hdpi-v4/ic_takeout_order_invalid.png'
# pic_path = '/private/tmp/all_china_53510/res/drawable-hdpi-v4/ic_takeout_order_refund.png'
# pic_path = '/private/tmp/all_china_53510/res/drawable-hdpi-v4/icon.png'
pic_path = '/private/tmp/all_china_53510/res/drawable-hdpi-v4/test.bmp'


# with open(pic_path, 'rb') as f:
#     img = f.read()
#     msg = client.basicGeneral(img)
#     for i in msg.get('words_result'):
#         print(i.get('words'))

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


def main():
    dir_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/drawable-xhdpi/'
    dir_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/'
    dir_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/'
    dir_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res'
    dir_path = '/Users/toutouhiroshidaiou/keruyun/proj/ios_proj/OnMobile/OnMobile/Assets.xcassets/'
    # dir_path = '/private/tmp/all_china_53510/res/'

    path_han = list()

    readed_file = set()

    try:
        for dir_path_name, dirs, files in os.walk(dir_path):
            # print(dir_path_name)
            # print(files)
            for f in files:
                if len(path_han) > 1500:
                    break

                path_of_dir = dir_path_name
                if not dir_path_name.endswith('/'):
                    path_of_dir += os.sep
                full_name = path_of_dir + f
                if full_name.endswith('.png'):
                    # print(os.path.isfile(full_name),full_name)

                    if readed_file.__contains__(full_name):
                        print(highlight('shit happen dup ', 4), full_name)
                        continue

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

        # git add .; git commit -m "auto upload"; git push origin i18n
        # os.chdir('/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/')
        # command = 'git add .; git commit -m "auto upload"; git push origin i18n'
        # exec_cmd(command)

    pass


if __name__ == '__main__':
    main()
