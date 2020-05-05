import os

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd, auto_transascii10
import re
import difflib

from org.ith.learn.work.Work import gener_dict_by_excel

"""
怎么知道新增哪些key
有一个基准 基准来源于apk包 生成中文的kce  从解压的apk中的values目录读取 values
values-zh values-zh-rCN values-zh-rHK values-zh-rTW  values

"""

dirs_need_care = [
    'values',
    'values-zh',
    'values-zh-rCN',
    'values-zh-rHK',
    'values-zh-rTW',
]


def gener_all_cn_by_apk(apk_path):
    # apk路径的上一级目录
    apk_path = apk_path.strip()
    print('apk_path ', apk_path)
    apk_parent = os.path.dirname(apk_path)
    apk_name = apk_path.split('/')[-1]
    os.chdir(apk_parent)
    command = 'apktool d ' + apk_path
    exec_cmd(command)
    res_path = apk_path.split('.')[0] + os.sep + 'res'
    print(res_path)
    care_path = list()
    for dir_path_name, dirs, files in os.walk(res_path):
        for name in dirs:
            if name in dirs_need_care:
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

    return out_path


def main():
    # old_path = gener_all_cn_by_apk('/private/tmp/envGrd/533app-official-armeabi-v7a-envGrd.apk')
    # new_path = gener_all_cn_by_apk('/private/tmp/envGrd/535app-official-armeabi-v7a-envGrd.apk')
    # diff_xml(new_path_xml=new_path, old_path_xml=old_path)

    diff_xml(new_path_xml='/private/tmp/envGrd/535app-official-armeabi-v7a-envGrd_apk_all_cn.xml',
             old_path_xml='/private/tmp/envGrd/533app-official-armeabi-v7a-envGrd_apk_all_cn.xml')

    # print(to_pretty('award_for_recommendation', '推荐有奖'))

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
                    line = 'changed key:{:<30}, from: {:<10}to: {}\n'.format(knew.key, kold.cn, knew.cn)
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
        tmp.append(new)

    # for old in old_diff:
    #     tmp.append(old)

    simple_new_name = new_path_xml.split('/')[-1].replace('.xml', '')
    simple_old_name = old_path_xml.split('/')[-1].replace('.xml', '')

    diff_out_name = out_path + '_diff_' + simple_old_name + simple_new_name + '.xml'

    write_kce_to_path(tmp, diff_out_name)

    out_del_change_add = '_delete_changed_newadd_' + simple_old_name + simple_new_name + '.xml'

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


def to_pretty(key, value):
    #     <string name="main_policy">售后政策</string>
    result = '\t<string name="{}">{}</string>'.format(key, value)
    return result


if __name__ == '__main__':
    main()
