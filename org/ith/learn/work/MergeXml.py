import os

from org.ith.learn.OhMyEXCEL import excel_to_xml
from org.ith.learn.util.PXML import write_kce_to_path, parse_string_as_kce
from org.ith.learn.util.TUtils import read_xml_as_kce_list, highlight, is_contains_chinese, exec_cmd, get_cur_branch
from org.ith.learn.util.Translator import to_simplized
from org.ith.learn.work.HardCode import hardcode_killer

"""
根据传入的module路径 merge一个包含所有中文英文繁体的key的xml 写入默认xml
"""

bak_cur_dir = '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/docs/'


def main():
    # hardcode_killer('/Users/lightman_mac/company/keruyun/proj_sourcecode/Dinner/')
    # do_merge()

    remote_kce_list = read_xml_as_kce_list('/tmp/master_string.xml')
    print('remote_kce_list size ', len(remote_kce_list))

    dinner_kce = read_xml_as_kce_list('../../../../docs/simple_dinner_string.xml')
    print('dinner_kce_list size ', len(dinner_kce))

    keys_of_remote = []
    for kce in remote_kce_list:
        keys_of_remote.append(kce.key)

    keys_of_dinner = []
    for kce in dinner_kce:
        keys_of_dinner.append(kce.key)

    diff = set(keys_of_remote) - set(keys_of_dinner)
    print('diff ', len(diff), diff)
    remiand = []
    for kce in remote_kce_list:
        if kce.key not in dinner_kce:
            remiand.append(kce)

    write_kce_to_path(remiand, '/tmp/except_dinner.xml')
    write_kce_to_path(dinner_kce, '/tmp/dinner.xml')


def do_merge():
    path_of_module = get_module_path('/Users/lightman_mac/company/keruyun/proj_sourcecode/Dinner')

    for module_path in path_of_module:
        if not module_path.__contains__('test'):
            clean_module(module_path)

    pass


def get_module_path(path):
    settings = 'settings.gradle'
    module_dirs = []

    remote = 'remotes/origin/develop'
    dest_local = 'develop'
    result = exec_cmd("git branch -a")
    cmd_switch = "git branch -b develop " + remote
    cmd_pull = 'git pull -r'

    for dir_path, dirs, files in os.walk(path):

        if settings in files:
            root_dir = dir_path
            os.chdir(root_dir)

            # 如果远端有develop 本地没有
            if result.__contains__(remote):
                #   判断当前是否为develop
                cur = get_cur_branch()
                if cur.strip() != dest_local:
                    exec_cmd(cmd_switch)

                exec_cmd(cmd_pull)

            # 读取settings.gradle文件获取需要的module
            with open(root_dir + os.sep + settings, 'r') as sg:
                # print("get_module_path", "path is ", root_dir + os.sep)
                modules = sg.readlines()
                for m in modules:
                    if m.__contains__('include') and not m.__contains__('//'):
                        file = m.split(':')[1].split('\'')[0]
                        module_dirs.append(root_dir + os.sep + file)
                return module_dirs


def check_branch():
    if get_cur_branch() != 'develop':
        exec_cmd("git checkout develop")
    exec_cmd("git pull -r")
    exec_cmd("git branch -D merge_test")
    exec_cmd("git checkout -b merge_test")


def clean_module(path_of_module):
    os.chdir(path_of_module)

    check_branch()

    main_res = 'res/values/strings.xml'
    list_of_values = list_res_values(path_of_module)
    biggest = []
    keys = []
    all_kv_dict = []

    main_res_path = ''

    for item in list_of_values:

        if main_res in item:
            main_res_path = item

        p_list = parse_string_as_kce(item)

        for p in p_list:

            all_kv_dict.append(p)

            # 生成包含所有key的biggest
            if p.key not in keys:
                biggest.append(p)
                keys.append(p.key)

    # 确保biggest里的kv v是中文
    for b in biggest:
        if not is_contains_chinese(b.cn):
            for al in all_kv_dict:
                if al.key == b.key and is_contains_chinese(al.cn):
                    b.cn = al.cn

    # 把biggest.xml的内容写入main_res.
    sorted(biggest)
    # str_of_big = ''
    os.chdir(bak_cur_dir)
    write_kce_to_path(biggest, './main_string.xml')

    for kce in biggest:
        kce.cn = to_simplized(kce.cn)

    write_kce_to_path(biggest, './simple_dinner_string.xml')

    # str_of_big = to_simplized(str_of_big)

    return main_res_path


def list_res_values(m_path):
    list_of_res = []
    for dir_path_name, dirs, files in os.walk(m_path):
        if dir_path_name.__contains__('values'):
            for file in files:
                if file.__contains__('strings'):
                    full_name = dir_path_name + '/' + file
                    list_of_res.append(full_name)
                    print(highlight(full_name))
    return list_of_res


if __name__ == '__main__':
    main()
