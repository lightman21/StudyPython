from org.ith.learn.OhMyEXCEL import xml_to_excel
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import read_xml_as_kce_list, is_contains_chinese, open_excel_as_list


def do_work():
    """
    根据传入的merge以后的资源 生成 kce列表
    """
    zh_path = '/tmp/th/my/res/values-zh/zh_string.xml'
    def_path = '/tmp/th/my/res/values/strings.xml'
    en_path = '/tmp/th/my/res/values-en/strings.xml'

    zh_kce_list = read_xml_as_kce_list(zh_path)
    def_kce_list = read_xml_as_kce_list(def_path)

    eng_kce_list = read_xml_as_kce_list(en_path)

    zh_keys = set()
    def_keys = set()

    for zh in zh_kce_list:
        zh_keys.add(zh.key)

    for zh in def_kce_list:
        def_keys.add(zh.key)

    zh_not_cn = []
    def_not_cn = []

    for zh in zh_kce_list:
        if zh.key not in def_keys:
            print(zh)

        if not is_contains_chinese(zh.cn):
            zh_not_cn.append(zh)

    for dd in def_kce_list:
        if not is_contains_chinese(dd.cn):
            def_not_cn.append(dd)

    # write_kce_to_path(zh_not_cn, './thtmp/zh_not_cn.xml')
    # write_kce_to_path(def_not_cn, './thtmp/def_not_cn.xml')
    # write_kce_to_path(zh_kce_list, './thtmp/zh_kce_list.xml')
    # write_kce_to_path(def_kce_list, './thtmp/def_kce_list.xml')

    for dkce in def_kce_list:
        for kce in zh_kce_list:
            if kce.key == dkce.key:
                if is_contains_chinese(kce.cn) and not is_contains_chinese(dkce.cn):
                    dkce.cn = kce.cn

    # write_kce_to_path(def_kce_list, './thtmp/def_kce_list.xml')
    # write_kce_to_path(eng_kce_list, './thtmp/eng_kce_list.xml')

    for kce in def_kce_list:
        for eng in eng_kce_list:
            if kce.key == eng.key:
                kce.en = eng.cn

    write_kce_to_path(def_kce_list, './thtmp/merged_total.xml')

    print('def_kce_list ', len(def_kce_list))
    print('eng_kce_list ', len(eng_kce_list))

    pass


def sw_rewrite():
    sw_list = open_excel_as_list('/Users/toutouhiroshidaiou/Desktop/tweak_0426_tang.xlsx')
    write_kce_to_path(sw_list, './thtmp/sw_rewrite_en.xml', key='en')
    write_kce_to_path(sw_list, './thtmp/sw_rewrite_cn.xml', key='cn')


def main():
    # do_work()
    # sw_rewrite()
    cn_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/work/thtmp/merged_total.xml'
    en_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/work/thtmp/all_eng_.xml'
    xml_to_excel(cn_path, en_path, './all_excel.xlsx')
    pass


if __name__ == '__main__':
    main()
