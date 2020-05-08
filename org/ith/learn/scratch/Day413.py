from org.ith.learn.OhMyEXCEL import excel_to_xml
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, is_contains_chinese

"""
git archive i18n_5.34.10 --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git app/src/main/res/values-en/strings.xml | tar -x

"""


def main():
    path_merge_def = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res/merged/official/envCiTest/values/values.xml'
    path_merge_cn = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res/merged/official/envCiTest/values-zh/values-zh.xml'
    out_cn = '/Users/lightman_mac/Desktop/tanghao/out_cn.xml'
    out_def = '/Users/lightman_mac/Desktop/tanghao/out_def.xml'
    out_merge = '/Users/lightman_mac/Desktop/tanghao/out_merge.xml'
    out_english = '/Users/lightman_mac/Desktop/tanghao/out_english.xml'
    def_list = read_xml_as_kce_list(path_merge_def)
    cn_list = read_xml_as_kce_list(path_merge_cn)
    # write_kce_to_path(def_list, out_def)
    # write_kce_to_path(cn_list, out_cn)

    now_en = '/Users/lightman_mac/company/keruyun/proj_sourcecode/mobile-storage/translate/kmobile/i18n.xml'

    key_merge_list = set()
    for kce in cn_list:
        key_merge_list.add(kce.key)

    for kce in def_list:
        key_merge_list.add(kce.key)

    print('total key size ', len(key_merge_list))

    for def_kce in def_list:
        for zh in cn_list:
            if def_kce.key == zh.key:
                if is_contains_chinese(zh.cn) and not is_contains_chinese(def_kce.cn):
                    def_kce.cn = zh.cn

    # write_kce_to_path(def_list, out_merge)
    # now_list = read_xml_as_kce_list(now_en)
    # write_kce_to_path(now_list, out_english)

    out_en_list = read_xml_as_kce_list(out_english)
    def_path_list = read_xml_as_kce_list('/Users/lightman_mac/Desktop/tanghao/out_merge.xml')

    key_oe = set()
    key_def = set()
    for kce in def_path_list:
        key_def.add(kce.key)

    for kce in out_en_list:
        key_oe.add(kce.key)

    not_i18n = list()
    for kce in def_path_list:
        if kce.key not in key_oe:
            not_i18n.append(kce)

    write_kce_to_path(not_i18n, '/Users/lightman_mac/Desktop/tanghao/not_i18n.xml')

    pass


def merge_kce_list(left_list, right_list):
    cn_merge_list = list()

    smaller = left_list
    bigger = right_list
    if len(left_list) > len(right_list):
        smaller = right_list
        bigger = left_list

    key_small = set()
    key_big = set()
    for kce in smaller:
        key_small.add(kce.key)
    for kce in bigger:
        key_big.add(kce.key)


if __name__ == '__main__':
    main()
