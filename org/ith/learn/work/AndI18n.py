import os
import time

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import read_xml_as_kce_list, KCEBean, highlight, \
    is_contains_chinese, exec_cmd, auto_transascii10, skip_key_prefix, write_to_excel
import re

"""
怎么知道新增哪些key
有一个基准 基准来源于apk包 生成中文的kce  从解压的apk中的values目录读取 values
values-zh values-zh-rCN values-zh-rHK values-zh-rTW  values
"""

china_dirs_need_care = [
    'values',
    'values-zh',
    'values-zh-rCN',
    'values-zh-rHK',
    'values-zh-rTW',
]

local_base_dir = '../../../../docs/i18n/'


def gener_all_cn_by_apk(apk_path):
    """
    返回生成的中文kce的路径
    """
    start = time.time()
    # apk路径的上一级目录
    apk_path = apk_path.strip()
    print('apk_path ', apk_path)
    apk_parent = os.path.dirname(apk_path)
    apk_name = apk_path.split('/')[-1]
    os.chdir(apk_parent)
    command = 'apktool d ' + apk_path
    exec_cmd(command)
    res_path = apk_path.split('.apk')[0] + os.sep + 'res'
    print(res_path)
    care_path = list()
    for dir_path_name, dirs, files in os.walk(res_path):
        for name in dirs:
            if name in china_dirs_need_care:
                care_path.append(dir_path_name + os.sep + name + os.sep + 'strings.xml')

    all_kce_list = list()
    def_kce_list = list()
    def_key_set = set()
    zh_kce_list = list()

    for path in care_path:

        kce_list = read_xml_as_kce_list(path)

        if path.__contains__('values/strings.xml'):
            def_kce_list = kce_list

        if path.__contains__('values-zh/strings.xml'):
            zh_kce_list = kce_list

        for kce in kce_list:
            all_kce_list.append(kce)

            if kce_list == def_kce_list:
                def_key_set.add(kce.key)

        print(path, ', size ', len(kce_list), ',all kce ', len(all_kce_list))

    diff_kce = set()
    for item in all_kce_list:
        if item.key not in def_key_set:
            # 这个就是多出来的
            diff_kce.add(item)

    print('def key set ', len(def_key_set), ',diff size ', len(diff_kce))

    for kce in diff_kce:
        def_kce_list.append(kce)

    not_cn_kce = list()
    for kce in def_kce_list:
        if not is_contains_chinese(kce.cn):
            not_cn_kce.append(kce)

    print(highlight('not_cn_kce size ', 2), len(not_cn_kce))

    count = 0
    # 不是中文 那么去 zh里查
    for zh_kce in zh_kce_list:
        for kce in not_cn_kce:
            if kce.key == zh_kce.key and is_contains_chinese(zh_kce.cn):
                kce.cn = zh_kce.cn
                count += 1

    print(highlight('not_cn_kce find in zh ', 3), count)

    # 如果还不行就到all里查
    count = 0
    for all_item in all_kce_list:
        for kce in not_cn_kce:
            if kce.key == all_item.key:
                if not is_contains_chinese(kce.cn) and is_contains_chinese(all_item.cn):
                    kce.cn = all_item.cn
                    count += 1

    print(highlight('not_cn_kce find in all_kce_list ', 4), count)

    for def_kce in def_kce_list:
        for kce in not_cn_kce:
            if kce.key == def_kce.key:
                def_kce.cn = kce.cn

    out_path = apk_parent + os.sep + apk_name.replace('.', '_') + '_all_cn.xml'
    write_kce_to_path(def_kce_list, path=out_path)

    end = time.time() - start
    print(highlight(', gener_all_cn_by_apk cost ', 2), end, ' s')
    return out_path


def pull_remote_dict():
    start = time.time()
    """
    拉取远端最新的english.xml文件
    """
    command = """
     git archive master --remote=ssh://git@gitlab.shishike.com:38401/OSMobile/mobile-storage.git translate/kmobile/english.xml | tar -x && cp translate/kmobile/english.xml {} && rm -rf translate
     """.format(local_base_dir)
    exec_cmd(command.strip())
    print('pull_remote_dict cost time ', (time.time() - start), 's')
    return read_xml_as_kce_list(local_base_dir + 'english.xml')


def main():
    pull_remote_dict()
    #
    # old_path = gener_all_cn_by_apk(
    #     '/private/tmp/arm_OnMobile-official-5.35.10-SNAPSHOT-armeabi-envGrd-2020-05-06-11-09-57.apk')
    # new_path = gener_all_cn_by_apk('/private/tmp/newest.apk')
    # diff_xml(new_path_xml=new_path, old_path_xml=old_path)
    # gener_all_cn_by_apk('/private/tmp/old.apk')
    # gener_all_cn_by_apk('/private/tmp/thOnMobile-official-5.36.0-SNAPSHOT-armeabi-v7a-envGrd-2020-05-09-08-42-21.apk')

    # check_apk_kce(
    #     '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/outputs/apk/official/envGrd'
    #     '/app-official-armeabi-v7a-envGrd.apk')

    apk_path = '/tmp/OnMobile-official-5.36.0-SNAPSHOT-armeabi-v7a-envSingapore-2020-05-11-10-04-19.apk'
    gener_excel_by_apk(apk_path)
    pass


def get_all_english_path_by_apk(path_of_apk):
    apk_path = path_of_apk.strip()
    print('apk_path english ', apk_path)
    apk_parent = os.path.dirname(apk_path)
    os.chdir(apk_parent)
    command = 'apktool d ' + apk_path
    exec_cmd(command)
    res_path = apk_path.split('.apk')[0] + os.sep + 'res/'
    en_flag = 'values-en'
    for dir_path_name, dirs, files in os.walk(res_path):
        if dir_path_name.endswith(en_flag):
            return dir_path_name + os.sep + 'strings.xml'
    pass


def gener_excel_by_apk(path_of_apk):
    start = time.time()
    path_of_china = gener_all_cn_by_apk(path_of_apk)
    path_of_english = get_all_english_path_by_apk(path_of_apk)
    print('in gener_excel_by_apk ', 'pwd ', os.curdir)
    tmpxml_to_excel(path_of_cn=path_of_china, path_of_en=path_of_english, excel_path='./Andi18n_5_36_0.xlsx')
    print('total cost ', (time.time() - start), ' s')
    pass


def check_apk_kce(path_of_apk):
    """
    @param 传入的apk路径
    反编译指定的apk并生成中文英文两个文件
    然后比较相同key有占位符的地方 是不是都一致 防止 手抖导致奔溃
    """
    cn_kce_path = gener_all_cn_by_apk(path_of_apk)
    english_path = get_all_english_path_by_apk(path_of_apk)

    dict_cn = dict()
    for kce in read_xml_as_kce_list(cn_kce_path):
        dict_cn[kce.key] = kce.cn
    dict_english = dict()
    for kce in read_xml_as_kce_list(english_path):
        dict_english[kce.key] = kce.cn

    cn_keys = dict_cn.keys()
    eng_keys = dict_english.keys()

    # setA & setB = set交集
    both_keys = cn_keys & eng_keys

    print('dict_cn size ', len(dict_cn), ',dict_english size ', len(dict_english), ',cn keys ', len(cn_keys),
          ',english keys ', len(eng_keys), ' both keys ', len(both_keys))

    cn_pop = list()

    tmp_dict = dict(dict_cn)
    for k, v in tmp_dict.items():
        if k not in both_keys:
            dict_cn.pop(k)
            cn_pop.append(KCEBean(key=k, cn=v, en=''))

    en_pop = list()

    tmp_dict = dict(dict_english)
    for k, v in tmp_dict.items():
        if k not in both_keys:
            dict_english.pop(k)
            en_pop.append(KCEBean(key=k, cn=v, en=''))

    check = '%'
    count = 0
    for key in both_keys:
        cn_v = str(dict_cn[key])
        en_v = str(dict_english[key])
        if cn_v.__contains__(check) and en_v.__contains__(check):
            # print(key, dict_cn[key])
            if cn_v.count(check) != en_v.count(check):
                print('===========================', highlight(key, 2), cn_v, highlight(en_v, 3))
            count += 1

        if cn_v.count('$') != en_v.count('$'):
            print('$$$$$$$', highlight(key, 4), cn_v, highlight(en_v, 5))

    print('both contains % ', count)

    tmp = set()
    for t in cn_pop:
        is_start_with = False
        for pre in skip_key_prefix:
            if str(t.key).startswith(pre):
                is_start_with = True
                break
        if not is_start_with:
            tmp.add(t)
            print('pre for loop ', t)
    # write_kce_to_path(list(tmp), './cn_pop.xml')
    # write_kce_to_path(en_pop, './english_pop.xml')
    pass


def diff_xml(new_path_xml, old_path_xml, out_path='/tmp/diffapk/'):
    """
    @param new_path_xml 新的xml路径
    @param old_path_xml 老的xml路径
    @param out_path 输出diff文件路径
    """
    new_list = read_xml_as_kce_list(new_path_xml)
    old_list = read_xml_as_kce_list(old_path_xml)

    both_set = set(new_list).intersection(set(old_list))

    new_diff = set(new_list) - both_set
    old_diff = set(old_list) - both_set

    key_new_diff = set()
    key_old_diff = set()

    for kce in new_diff:
        key_new_diff.add(kce.key)

    for kce in old_diff:
        key_old_diff.add(kce.key)

    # 新增的 在新的但是不在老的
    kce_new_added = list()
    str_new_added_line = list()

    for knew in new_diff:
        if knew.key not in key_old_diff:
            if str(knew.key).startswith('leak_canary_'):
                continue
            kce_new_added.append(knew)
            line = 'new added {} , {}\n'.format(knew.key, knew.cn)
            line = to_pretty(knew.key, auto_transascii10(knew.cn)) + '\n'
            str_new_added_line.append(line)
            # print(line)

    # 变动的 key都在 但是value不同
    str_changed_line = list()
    kce_changed_value = list()
    for knew in new_diff:
        for kold in old_diff:
            if knew.key == kold.key:
                if knew.cn != kold.cn:
                    kce_changed_value.append(knew)
                    line = 'changed key:{:<30}, from: {:<10}  to: {}\n'.format(knew.key, kold.cn, knew.cn)
                    str_changed_line.append(line)
                    # print(line)

    delete_strs = list()

    for kold in old_diff:
        if kold.key not in key_new_diff:
            # line = 'delete key {} {}\n'.format(kold.key, kold.cn)
            line = to_pretty(kold.key, kold.cn) + '\n'
            print(highlight(line, 3))
            delete_strs.append(line)

    print(highlight('new added count', 4), len(kce_new_added), highlight(',changed count ', 5), len(kce_changed_value))

    desc = ''.format(len(delete_strs), len(kce_new_added), len(kce_changed_value))

    tmp = list()
    for new in new_diff:
        new.cn = auto_transascii10(new.cn)
        if not str(new.key).startswith('leak_canary_'):
            tmp.append(new)

    # for old in old_diff:
    #     tmp.append(old)

    simple_new_name = new_path_xml.split('/')[-1].replace('.xml', '')
    simple_old_name = old_path_xml.split('/')[-1].replace('.xml', '')

    diff_out_name = out_path + '_diff_' + simple_old_name + simple_new_name + '.xml'

    write_kce_to_path(tmp, diff_out_name)

    out_del_change_add = out_path + '_delete_changed_newadd_' + simple_old_name + simple_new_name + '.xml'

    out_lines = list()
    out_lines.append('deleted:\n')
    out_lines.extend(delete_strs)
    out_lines.append('\n\nchanged:\n')
    out_lines.extend(str_changed_line)
    out_lines.append('\n\nnew added:\n')
    out_lines.extend(str_new_added_line)

    print('out_del_change_add', out_del_change_add)

    with open(out_del_change_add, 'w') as rout:
        rout.writelines(out_lines)

    # with open(changed_out_name, 'w') as rout:
    #     rout.writelines(str_changed_line)
    # with open(newadd_out_name, 'w') as rout:
    #     rout.writelines(str_new_added_line)


def gener_commented_english(cn_path, eng_path, out_path='tmp/comment_en.xml'):
    """
    根据传入的全中文全英文 生成带注释的英文xml
    如 <!--    关于 --> 	<string name="aboutus_title">about</string>
    """
    cn_list = read_xml_as_kce_list(cn_path)
    left = '<!--'
    right = '-->'
    str_en_line = list()
    with open(eng_path, 'r') as rin:
        lines = rin.readlines()
        count = 0
        for line in lines:
            if count < 30000:
                match = r'<string name="(\w*)">(.*)</string>'
                rets = re.findall(match, line, re.DOTALL)
                if len(rets) > 0:
                    rets = rets[0]
                    key = rets[0]
                    value = rets[1]
                    count += 1
                    kce = find_kce_by_key(key, cn_list)
                    if kce is None:
                        print('shit kce none key is ', key)
                        continue
                    ss = '{} {} {} {}'.format(left, kce.cn.replace('--', '__'), right, line)
                    str_en_line.append(ss)

        with open(out_path, 'w') as rout:
            rout.writelines(str_en_line)
    pass


def find_kce_by_key(key, kce_list):
    for kce in kce_list:
        if kce.key == key:
            return kce


def to_pretty(key, value):
    #     <string name="main_policy">售后政策</string>
    result = '\t<string name="{}">{}</string>'.format(key, value)
    return result


def tmpxml_to_excel(path_of_cn, path_of_en, excel_path):
    """
    """
    cn_list = read_xml_as_kce_list(path_of_cn, 'cn')
    en_list = read_xml_as_kce_list(path_of_en, 'en')

    tmp = list(cn_list)
    for kce in tmp:
        for skip in skip_key_prefix:
            if str(kce.key).startswith(skip):
                if cn_list.__contains__(kce):
                    cn_list.remove(kce)

    tmp = list(en_list)
    for kce in tmp:
        for skip in skip_key_prefix:
            if str(kce.key).startswith(skip):
                if en_list.__contains__(kce):
                    en_list.remove(kce)

    for item in cn_list:
        for en_item in en_list:
            if item.key == en_item.key:
                item.en = en_item.en
    list_dup = []
    dict_cd = dict()
    count = 0
    for cn in cn_list:
        if dict_cd.__contains__(cn.cn):
            list_dup.append(cn)
            count += 1
        else:
            dict_cd[cn.cn] = cn.key

    print(highlight('duplicate count '), count, 'total size ', len(cn_list))
    write_to_excel(cn_list, excel_path)


if __name__ == '__main__':
    main()
