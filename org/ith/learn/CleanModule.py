import os
import re

from org.ith.learn.util.PXML import parse_string_as_kce, write_kce_to_path
from org.ith.learn.util.TUtils import exec_cmd, is_contains_chinese, KCEBean, read_xml_as_kce_list, highlight
from org.ith.learn.util.Translator import to_simplized


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
        modules = get_module_path(dir_path_name)
        if modules is not None:
            for mod in modules:
                name = (mod + res_dir)
                list_res_values(name)


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


def get_module_properties(m_path):
    """
    获取module的gradle.properties
    gradle.properties', 'gradlew.bat', 'settings.gradle
    """
    for dir_path_name, dirs, files in os.walk(m_path):
        if 'settings.gradle' in files and 'gradle.properties' in files:
            return dir_path_name + 'gradle.properties'


def get_cur_branch():
    ret = exec_cmd("git branch | grep \\* | awk '{print$2}'")
    return ret.strip()


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
    exec_cmd("git branch -D i18n")
    exec_cmd("git checkout -b i18n")


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
    str_of_big = ''
    # str_of_big = to_simplized(str_of_big)
    # write_kce_to_path(biggest, main_res_path)


    # # 修改properties版本号
    # modify_properties(path_of_module)

    # 执行upload 即编译
    # build_module(path_of_module)

    # 删除其他values
    # for other in list_of_values:
    #     if not other.__contains__(main_res):
    #         os.remove(other)

    # commit
    # exec_cmd('git add .; git commit -m "remove values except default" ')

    return main_res_path


def build_module(m_path):
    os.chdir(m_path)
    exec_cmd("./gradlew uploadArchives")


def modify_properties(m_path='/tmp/tmp/Dinner/', v_code=12345, v_name="1.23.45"):
    """
    VERSION_NAME=2.25.50
    VERSION_CODE=2025050
    """
    prop_path = get_module_properties(m_path)
    print(prop_path)
    with open(prop_path, 'r') as file:
        origin_lines = file.readlines()
        new_lines = []
        for line in origin_lines:
            tmp = line
            if tmp.startswith('VERSION_NAME'):
                tmp = "VERSION_NAME=" + str(v_name) + os.linesep
            if tmp.startswith('VERSION_CODE'):
                tmp = "VERSION_CODE=" + str(v_code) + os.linesep
            new_lines.append(tmp)
        with open(prop_path, 'w') as wf:
            wf.writelines(new_lines)


def main():
    clean_module('/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/Dinner/')


def old():
    en_path = '/Userxs/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values-en/strings' \
              '.xml'
    en_list = read_xml_as_kce_list(en_path, lang='en')
    cn_path = '/Users/lxightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values/strings.xml'
    cn_list = read_xml_as_kce_list(cn_path, lang='cn')

    for cn in cn_list:
        for en in en_list:
            if cn.key == en.key:
                cn.en = en.en
                en.cn = cn.cn

    list_ios_kce = get_ios_kces()

    skip = ['年', '月', '周', '日', '时', '分', '秒']
    tmp = []
    count = 0
    for ios in list_ios_kce:
        if ios.cn not in skip:
            tmp.append(ios)

    list_ios_kce.clear()
    list_ios_kce.extend(tmp)

    count = 0
    for enitem in en_list:
        for ios in list_ios_kce:
            if enitem.cn == ios.cn:
                if enitem.en != ios.en:
                    enitem.en = ios.en
                    count += 1

    for en in en_list:
        en.cn = ''
        print(en)
    write_kce_to_path(en_list, en_path, key='en')

    print("中文一样 但是英文不一样 ", count)
    # write_to_excel(cn_list, './th_merged.xlsx')

    # 让所有的en都有对应中文
    # for en in en_list:
    #     for cn in cn_list:
    #         if cn.key == en.key:
    #             en.cn = cn.cn

    # cn_en_dict = dict()
    # count = 0
    # for english in en_list:
    #     en_v = str(english.en)
    #     chn_v = str(english.cn)
    #     # 中文一样 英文不一样
    #     if not cn_en_dict.__contains__(chn_v):
    #         cn_en_dict[chn_v] = en_v
    #     else:
    #         # 把对应中文的英文写入 对应item
    #         count += 1
    #         english.en = cn_en_dict[chn_v]

    # for en in en_list:
    #     en.cn = ''
    #     print(en)
    # write_kce_to_path(en_list, en_path, key='en')

    # write_to_excel(cn_list, './after_dup.xlsx')


def get_ios_kces():
    ios_p = '/Users/lightman_mac/Desktop/i18n_values-en/ios_en.strings.java'
    en_kce = read_ios_as_kce_list(ios_p)
    ios_p = '/Users/lightman_mac/Desktop/i18n_values-en/ios_cn.strings.java'
    cn_kce = read_ios_as_kce_list(ios_p)
    print(len(en_kce), len(cn_kce))
    ios_kces = list()
    for en in en_kce:
        for cn in cn_kce:
            if en.key == cn.key:
                tmp = en.cn
                ios_kces.append(KCEBean(key=en.key, cn=cn.cn, en=tmp))

    for ios in ios_kces:
        ios.en = ios.en.strip().replace('\'', '\\\'')

    return ios_kces


def read_ios_as_kce_list(ios_path):
    with open(ios_path, 'r') as file:
        all_str = file.read()
        ios_match = r'"(.*)"\s=\s"(.*)"'
        list_kce = []
        rets = re.findall(ios_match, all_str)
        for t in rets:
            h = KCEBean(key=t[0], cn=t[1], en='')
            list_kce.append(h)

        return list_kce


def do_diff():
    # dinner 里的所有key 是不是在主工程中包含了
    print("hello")
    # clean_module('/Users/lightman_mac/company/keruyun/proj_sourcecode/mobile-trade-server/')

    d_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/mobile-trade-server/TradeServer/src/main/res/values' \
             '/strings.xml'
    dinner_list = read_xml_as_kce_list(d_path, lang='cn')
    main_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/Dinner/dinnerui/src/main/res/values/strings.xml'
    main_list = read_xml_as_kce_list(d_path, lang='cn')
    km = []
    for m in main_list:
        km.append(m.key)
    for dinner in dinner_list:
        if dinner.key not in km:
            print('not in main', dinner)

    print('done')


if __name__ == '__main__':
    main()
