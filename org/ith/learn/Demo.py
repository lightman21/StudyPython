import os

import colored as colored

from org.ith.learn.PXML import parse_string_as_kce, write_kce_to_path


def write_demo():
    # 遍历目录
    path = "/Users/lightman_mac/company/keruyun/proj_sourcecode/Dinner/dinnerui/src/main/res"

    out_path = "../../../docs/tmmp/"

    # walk方法会返回一个三元组，分别是root、dirs和files
    # 目录名称  目录下的目录 目录里的文件list<string>

    biggest = []
    biggest_key = []
    ch_list = []

    for dir_path_name, dirs, files in os.walk(path):

        if dir_path_name.__contains__('values'):
            base = dir_path_name.split("/")[-1]

            for file in files:
                if file.__contains__('strings'):
                    full_name = dir_path_name + '/' + file

                    # print(full_name)

                    p_list = parse_string_as_kce(full_name)
                    out = out_path + base + '___string.xml'
                    write_kce_to_path(p_list, os.path.abspath(out))

                    if full_name.__contains__('values-zh'):
                        ch_list = p_list

                    simple_name = full_name[full_name.index('res'):]

                    print(full_name, "keys ", len(p_list))

                    for f in p_list:
                        if not biggest_key.__contains__(f.key):
                            biggest.append(f)
                            biggest_key.append(f.key)

    print("total key s ", len(biggest), len(ch_list))

    for big in biggest:
        for ch in ch_list:
            if ch.key == big.key:
                big.cn = ch.cn

    write_kce_to_path(biggest, out_path + "biggest.xml")


def find_not_match(path_of_module):
    """
    找出指定module目录下 string.xml文件不匹配的情况
    :param path_of_module:     module_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/Dinner'
    :return:
    """

    for dir_path_name, dirs, files in os.walk(path_of_module):
        res_dir = '/src/main/res'
        ll = get_module_path(dir_path_name)
        # print("dir_path_name", dir_path_name, "ll " + str(ll))
        if ll is not None:
            for l in ll:
                name = (l + res_dir)
                print("start parse ", l)
                list_res_values(name)


def highlight(str_line):
    CRED = '\033[93m'
    CEND = '\033[0m'
    return '{} {} {}'.format(CRED, str_line, CEND)


def list_res_values(path):
    for dir_path_name, dirs, files in os.walk(path):
        if dir_path_name.__contains__('values'):
            base = dir_path_name.split("/")[-1]
            for file in files:
                if file.__contains__('strings'):
                    full_name = dir_path_name + '/' + file
                    p_list = parse_string_as_kce(full_name)

                    print(full_name, highlight("\tkce size "), len(p_list))
    print()


def get_module_path(path):
    root_dir = ''
    settings = 'settings.gradle'
    module_dirs = []
    for dir_path_name, dirs, files in os.walk(path):
        if settings in files:
            root_dir = dir_path_name
            # 读取settings.gradle文件获取需要的module
            with open(root_dir + os.sep + settings, 'r') as sg:
                modules = sg.readlines()
                print(''.join(modules))
                for m in modules:
                    if m.__contains__('include') and not m.__contains__('//'):
                        file = m.split(':')[1].split('\'')[0]
                        module_dirs.append(root_dir + os.sep + file)
                return module_dirs


import requests
import json


def gitlab():
    body = {}
    url = 'http://gitlab.shishike.com/groups/c_iphone/-/children.json?page=4'
    headers = {
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Cookie': "sidebar_collapsed=false; __utmz=88038286.1580971726.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=("
                  "none); __utma=88038286.1460782901.1580971726.1584367992.1585327915.11; "
                  "remember_user_token"
                  "=W1s4NjFdLCIkMmEkMTAkMHdtaEM0ckpDUDZjSk5rbFo5ZTFyTyIsIjE1ODU1Nzg1OTAuMjg3MDA3Il0%3D"
                  "--973f22857312ff21d733523deafc897321268556; _gitlab_session=6c43f845a0e5db7606c204183e77f25d",
        'Host': "gitlab.shishike.com",
        'Pragma': "no-cache",
        'Referer': "http://gitlab.shishike.com/c_iphone",
        'User-Agent': "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36",
        'X-CSRF-Token': "7gQxJ/3DA2dPC4zwxasA/Tjfg2qPYrNudksvtQeTaoubc9aVvGpFKzMrEId9RpS3kMFV5NBK+vnL+H+sFxQdCA==",
        'X-Requested-With': "XMLHttpRequest"
    }

    response = requests.get(url, data=json.dumps(body), headers=headers)
    resp = (response.json())
    print(len(resp))
    res = os.system('ls -l')
    print(type(res))


if __name__ == '__main__':
    # module_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/'
    # find_not_match(module_path)
    gitlab()
