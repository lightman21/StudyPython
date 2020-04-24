import os
import sys
import time

from org.ith.learn.CleanModule import clean_module, read_ios_as_kce_list
from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd
import re
import difflib

from org.ith.learn.work.HardCode import hardcode_killer


def search_kce(search, compare_by='cn', dict_path='../../../../docs/dicts/2020_04_20_kce_dict.xml',
               up_threshold=1.0,
               down_thread=0.9
               ):
    with open(dict_path, 'r') as rin:
        lines = rin.readlines()
        pattern = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
        for line in lines:
            rets = re.findall(pattern, line)
            rets = rets[0]
            kce = KCEBean(key=rets[0], cn=rets[1], en=rets[2])
            if compare_by == 'key':
                if down_thread <= approximately_equal_to(kce.key, search) <= up_threshold:
                    # if kce.key == search:
                    return kce
            elif compare_by == 'en':
                if down_thread <= approximately_equal_to(kce.en, search) <= up_threshold:
                    # if kce.en == search:
                    return kce
            else:  # 比cn默认
                if down_thread <= approximately_equal_to(kce.cn, search) <= up_threshold:
                    # if kce.cn == search:
                    return kce


def approximately_equal_to(s1, s2):
    s1 = remove_punctuation(s1).replace(' ', '')
    s2 = remove_punctuation(s2).replace(' ', '')
    return difflib.SequenceMatcher(lambda x: x in ':：！!?。', s1, s2).quick_ratio()


def work():
    string = '<kce key="about_text" cn="关于" en="About" />'
    matcher = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
    rets = re.findall(matcher, string)
    print(rets)

    big_kce_list = big_dict()
    cn_set = set()
    no_dup = list()
    for big in big_kce_list:
        print(big)
        if big.cn not in cn_set:
            cn_set.add(big.cn)
            no_dup.append(big)

    print('big size ', len(big_kce_list), ', cn size ', len(cn_set))
    now_date = time.strftime("%Y_%m_%d", time.localtime())
    to_write_lines = []
    for kce in no_dup:
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            v_cn = auto_escape(kce.cn).replace('please', 'pls').replace('Please', 'Pls').capitalize()
            v_en = auto_escape(kce.en).capitalize()
            line = '<kce key="{:<40}" cn="{}" en="{}"/>\n'.format(kce.key, v_cn, v_en)
            to_write_lines.append(line)

    with open('./{}_kce_dict.xml'.format(now_date), 'w') as out:
        out.writelines(to_write_lines)

    pass


def gener_diff(new_path, old_path, diff_path='./diff_old_new_2.xml'):
    kce_list_new = read_xml_as_kce_list(new_path)
    kce_list_old = read_xml_as_kce_list(old_path)
    key_olds = []
    for kce in kce_list_old:
        key_olds.append(kce.key)

    diff_kce = set()
    count = 0

    for new in kce_list_new:
        if new.key not in key_olds:
            # if not str(new.key).__contains__('autogen'):
            #     if not str(new.key).__contains__('takeout_'):
            if not str(new.key).__contains__('leak_canary_'):
                diff_kce.add(new)

        for old in kce_list_old:
            if old.key == new.key and old.cn != new.cn:
                diff_kce.add(new)

    print('old len ', len(kce_list_old), ',new len ', len(kce_list_new))
    print(', diff count ', count)
    write_kce_to_path(diff_kce, diff_path)


def main(argv=None):
    """
        首页
        个人中心
        桌台点单
        快速点单
        报表
        商品管理
    # gener_dict_by_excel('/Users/toutouhiroshidaiou/Desktop/i18n/0421_i18n.xlsx')
    # gener_dict_by_excel('/Users/toutouhiroshidaiou/Desktop/km2008.xlsx')
    """
    if argv is None:
        argv = sys.argv

    # clean_module('/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/mobile-trade-server/')

    module_path = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-commodity/'
    module_path = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/KReport/'
    hardcode_killer(module_path)

    # just_sort('/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-commodity/commodity/src/main/res/values/strings.xml')
    # just_sort('/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-commodity/commodity/src/main/res/values-en/strings.xml')


def just_sort(path_of_xml):
    kce_list = read_xml_as_kce_list(path_of_xml)
    write_kce_to_path(kce_list, path_of_xml)


def delete_res():
    # clean_module()
    # module_path = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/Dinner/'
    # module_path = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/mobile-trade-server/'
    # module_path = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-commodity/'
    # module_path = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/KReport/'
    # clean_module(module_path)

    # trans_module('../../../../docs/pure/dinner_string.xml')
    # trans_module('../../../../docs/pure/kreport.xml')

    tmp_path = '../../../../docs/pure/dinner_string.xml'
    master_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values' \
                  '/strings.xml'
    tmp_list = read_xml_as_kce_list(tmp_path)
    master_list = read_xml_as_kce_list(master_path)
    count = 0
    to_delete = []
    for m in master_list:
        for tmp in tmp_list:
            if m.key == tmp.key:
                count += 1
                to_delete.append(m.key)

    print('to_delete count', count, ',origin dinner count ', len(tmp_list))

    to_master = list()
    for m in master_list:
        if m.key in to_delete:
            to_master.append(m)
    write_kce_to_path(tmp_list, '/tmp/dinner_origin.xml')


def trans_module(str_path):
    diff_list = read_xml_as_kce_list(str_path)
    find_list = []
    not_find_list = []
    count = 0

    dict_path = '../../../../docs/dicts/2020_04_22_kce_dict.xml'
    dict_kce = dict()
    with open(dict_path, 'r') as rin:
        lines = rin.readlines()
        pattern = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
        for line in lines:
            rets = re.findall(pattern, line)
            rets = rets[0]
            kce = KCEBean(key=rets[0], cn=rets[1], en=rets[2])
            dict_kce[kce.key.strip()] = kce

    for diff in diff_list:
        to_search = diff.key
        ret = dict_kce.get(diff.key.strip())

        if ret is not None:
            count += 1
            find_list.append(ret)
            # print('search ', highlight(diff.cn, 3), ',return ' + ret.hl())
        else:
            not_find_list.append(diff)

    print('total diff ', len(diff_list), ',find ', count)

    for kce in not_find_list:
        print(kce.hl())

    with open('/Users/lightman_mac/Desktop/tmp/n_diff_find.xml', 'w') as rout:
        find_list = to_dict_item(find_list)
        rout.writelines(find_list)
    write_kce_to_path(not_find_list, '/Users/lightman_mac/Desktop/tmp/n_diff_not_find.xml')


def translate():
    new_path = '/Users/toutouhiroshidaiou/tmp/new_535_/res/values/strings.xml'
    old_path = '/Users/toutouhiroshidaiou/tmp/old_534.apk/res/values/strings.xml'
    gener_diff(new_path, old_path)

    diff_list = read_xml_as_kce_list('diff_old_new_2.xml')
    count = 0

    find_list = []
    not_find_list = []

    for diff in diff_list:
        ret = search_kce(diff.cn, down_thread=1.0,
                         dict_path='/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/docs/dicts'
                                   '/2020_04_21_kce_dict.xml')
        if ret is not None:
            count += 1
            find_list.append(ret)
            print('search ', highlight(diff.cn, 3), ',return ' + ret.hl())
        else:
            not_find_list.append(diff)

    print('total diff ', len(diff_list), ',find ', count)

    with open('./diff_find.xml', 'w') as rout:
        find_list = to_dict_item(find_list)
        rout.writelines(find_list)
    write_kce_to_path(not_find_list, './diff_not_find.xml')


def gener_dict_by_excel(path_of_excel, just_return=False):
    (cn_out_path, en_out_path) = excel_to_xml(path_of_excel)
    cn_list = read_xml_as_kce_list(cn_out_path)
    eng_list = read_xml_as_kce_list(en_out_path)
    merge_list = []
    key_cn_dict = dict()

    """
    <kce key="table_has_buffet              " cn="自助餐订单请到pos操作" en="Buffet order pls go to pos operation"/>
    <kce key="table_has_groupon             " cn="团餐订单请到pos操作" en="Operate group meal on pos"/>
    """

    for cn in cn_list:
        if is_contains_chinese(cn.key):
            cn.key = md5(cn.key)

    for en in eng_list:
        if is_contains_chinese(en.key):
            en.key = md5(en.key)

    for k in cn_list:
        key_cn_dict[k.key] = k.cn

    for eng in eng_list:
        if eng.key in key_cn_dict.keys() and len(eng.cn) > 0:
            eng.en = eng.cn
            eng.cn = key_cn_dict[eng.key]
            merge_list.append(eng)

    if just_return:
        return merge_list

    to_write_lines = to_dict_item(merge_list)
    now_date = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
    out_name = '../../../docs/{}_{}_kce_dict.xml'.format(now_date, path_of_excel.split('/')[-1])
    with open(out_name, 'w') as out:
        out.writelines(to_write_lines)


def to_dict_item(kce_list):
    """
    自助餐订单请到POS操作
    .capitalize()
    自助餐订单请到pos操作
    """
    to_write_lines = []
    for kce in kce_list:
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            v_cn = auto_escape(kce.cn).replace('please', 'pls').replace('Please', 'Pls')
            v_en = auto_escape(kce.en)
            v_key = md5(kce.key) if is_contains_chinese(kce.key) else kce.key
            # res = 'zuo' if x > y else 'you'.
            line = '<kce key="{:<30}" cn="{}" en="{}"/>\n'.format(v_key, v_cn, v_en)
            to_write_lines.append(line)

    return to_write_lines


if __name__ == '__main__':
    main()
