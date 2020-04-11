import os
import sys

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, KCEBean, exec_cmd, highlight, read_xml_as_kce_list, \
    write_to_excel

"""git archive --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git 
HEAD:app/src/main/res/values-en/ strings.xml | tar -x && cp strings.xml ~/th_strings.xml && rm strings.xml 

"""


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # cn_en_tuple = excel_to_xml('/Users/lightman_mac/Desktop/0411work/panshuangwei_0410_origin.xlsx', '/tmp/i18n/')
    ce_dict = gener_cn_en_dict('/Users/lightman_mac/Desktop/0411work/panshuangwei_0410_origin.xlsx')
    print(len(ce_dict))


def xml_to_excel(path_of_cn, path_of_en, excel_path):
    """
    """
    cn_list = read_xml_as_kce_list(path_of_cn, 'cn')
    en_list = read_xml_as_kce_list(path_of_en, 'en')

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


def excel_to_xml(path_of_excel, xml_path='../../../docs/'):
    """
    把excel的数据分成两个xml
    """
    list_kce = open_excel_as_list(path_of_excel)
    cn_list = []
    en_list = []

    print('path_of_excel:', path_of_excel)

    excel_name = path_of_excel.split('/')[-1].replace('.', '')

    for kce in list_kce:
        if len(kce.cn) > 0:
            cn_list.append(KCEBean(key=kce.key, cn=kce.cn, en=''))
        if len(kce.en) > 0:
            en_list.append(KCEBean(key=kce.key, cn='', en=kce.en))

    en_out_path = xml_path + excel_name + '_english.xml'
    cn_out_path = xml_path + excel_name + '_china.xml'

    log = 'excel_to_xml cn size ' + str(len(cn_list)) + ', en size ' + str(len(en_list))
    print(highlight(log, 2))

    write_kce_to_path(list_of_kce=en_list, path=en_out_path, key='en')
    write_kce_to_path(list_of_kce=cn_list, path=cn_out_path, key='cn')

    return cn_out_path, en_out_path


def gener_cn_en_dict(path_of_excel):
    list_kce = open_excel_as_list(path_of_excel)
    cn_en_dict = dict()
    for kce in list_kce:
        if len(kce.cn) > 0 and len(kce.en) > 0:
            cn_en_dict[kce.cn] = kce.en

    return cn_en_dict


if __name__ == "__main__":
    sys.exit(main())
