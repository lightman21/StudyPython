import os

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight


def main():
    # path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/KReport'
    path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/kmobile-android-inventory-management'
    path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/kmobile-commodity'
    path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/Dinner'
    path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/mobile-trade-server'
    path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/kmobile-member-manage'
    p = '/Users/lightman_mac/company/keruyun/proj_sourcecode/kmobile-member-manage/kmember/src/main/res/values/strings.xml'
    # merge_en_string(path)

    find_trans(p)

    # ready()
    pass


def find_trans(input_path):
    input_list = read_xml_as_kce_list(input_path)

    dest_path = '/Users/lightman_mac/Desktop/0418work/dict_418.xml'
    all_kces = []
    with open(dest_path, 'r') as rin:
        lines = rin.readlines()
        for li in lines:
            k = li.split('==')
            all_kces.append(KCEBean(key=k[0].strip(), cn=k[1].strip(), en=k[2].strip()))

    find_set = set()
    cn_find_set = set()

    for kin in input_list:
        if str(kin.key).__contains__('_autogen_'):
            finded = find_in_list(kin.cn, all_kces)
            if finded:
                if finded.cn not in cn_find_set:
                    find_set.add(finded)
                    cn_find_set.add(finded.cn)
                    print(finded)

    not_trans = []
    count = 0
    for kce in input_list:
        if str(kce.key).__contains__('_autogen'):
            count += 1
            not_trans.append(kce)

    print('total count ', count, ',and find set ', len(find_set), cn_find_set)
    real_not = []
    for notr in not_trans:
        if notr.cn not in cn_find_set:
            real_not.append(notr)
            print(highlight(notr.cn, 2))

    not_trans.clear()
    not_trans = real_not

    cnpath = './cn_trans.xml'
    enpath = './en_trans.xml'

    write_kce_to_path(not_trans, cnpath)

    for kce in not_trans:
        kce.cn = ''

    write_kce_to_path(not_trans, enpath)
    # path_of_cn, path_of_en, excel_path
    xml_to_excel(path_of_cn=cnpath, path_of_en=enpath, excel_path='./not_i18n.xlsx')


def find_in_list(cn_value, list_kce):
    for kce in list_kce:
        if kce.cn == cn_value:
            return kce


def merge_en_string(path_of_module):
    # 先读取当前的string

    print('path_of_module', path_of_module)
    dt = '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/docs/no_trans/'
    out_no_path = dt + path_of_module.split('/')[-1] + '_not_trans.xml '

    big_en_list = read_xml_as_kce_list('/Users/lightman_mac/Desktop/en_kce418.xml')
    en_path = get_en_path(path_of_module)
    cn_path = get_default_path(path_of_module)

    module_en_list = read_xml_as_kce_list(en_path)
    module_cn_list = read_xml_as_kce_list(cn_path)

    print('cn path ', cn_path)

    keys_module = set()
    keys_big = set()

    to_write_kce = []

    for kce in module_en_list:
        keys_module.add(kce.key)
        to_write_kce.append(kce)

    for kce in big_en_list:
        keys_big.add(kce.key)

    not_trans = []

    for kce in module_en_list:
        if kce.key not in keys_big:
            big_en_list.append(kce)

            not_trans.append(kce)

    write_kce_to_path(big_en_list, en_path)

    for kce in not_trans:
        kce.en = kce.cn
        kce.cn = ''

    for kce in not_trans:
        for cn in module_cn_list:
            if kce.key == cn.key:
                kce.cn = cn.cn

    lines = ['\n' * 5]
    for kce in not_trans:
        line = '{:<40} {:<30} {:<30}\n'.format(kce.key, kce.cn, kce.en)
        lines.append(line)

    with open(out_no_path, 'w') as out:
        out.writelines(lines)


def get_en_path(path_module):
    en_path = 'values-en'

    # 主module
    main_res = 'res/values-en'

    list_p = get_module_path(path_module)
    for lp in list_p:
        print('list_p', list_p)
        list_res = list_res_values(lp)

        print('list_res', list_res)

        for res in list_res:
            if not res.__contains__('test') and not res.__contains__('demo'):
                if res.__contains__(en_path):
                    return res


def get_default_path(path_module):
    def_path = 'res/values/strings.xml'
    list_p = get_module_path(path_module)
    for lp in list_p:
        list_res = list_res_values(lp)
        for res in list_res:
            if not res.__contains__('test') and not res.__contains__('demo'):
                if res.__contains__(def_path):
                    return res


def list_res_values(m_path):
    list_of_res = []
    for dir_path_name, dirs, files in os.walk(m_path):
        if dir_path_name.__contains__('values'):
            for file in files:
                if file.__contains__('strings'):
                    full_name = dir_path_name + '/' + file
                    list_of_res.append(full_name)
    return list_of_res


def ready():
    new_excel_path = '/Users/lightman_mac/Desktop/0418work/418_i18n.xlsx'
    kce_list = open_excel_as_list(new_excel_path)
    dest_path = '/Users/lightman_mac/Desktop/0418work/dict_418.xml'

    lines = []
    for kce in kce_list:
        line = '{:<40} == {:<30} == {:<20}\n'.format(kce.key, kce.cn, kce.en)
        lines.append(line)

    with open(dest_path, 'w') as out:
        out.writelines(lines)

    en_path = '/Users/lightman_mac/Desktop/en_kce418.xml'
    write_kce_to_path(kce_list, path=en_path, key='en')


def get_module_path(path):
    settings = 'settings.gradle'
    module_dirs = []

    for dir_path, dirs, files in os.walk(path):

        if settings in files:
            root_dir = dir_path
            os.chdir(root_dir)

            # 读取settings.gradle文件获取需要的module
            with open(root_dir + os.sep + settings, 'r') as sg:
                # print("get_module_path", "path is ", root_dir + os.sep)
                modules = sg.readlines()
                for m in modules:
                    if m.__contains__('include') and not m.__contains__('//'):
                        file = m.split(':')[1].split('\'')[0]
                        module_dirs.append(root_dir + os.sep + file)
                return module_dirs


if __name__ == '__main__':
    main()
