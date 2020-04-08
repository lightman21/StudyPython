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

    # path_excel = '../../../docs/android_i18n_0407.xlsx'
    # excel_to_xml(path_excel, '/tmp/')
    cn_p = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values/strings.xml'
    en_p = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values-en/strings.xml'
    excel_path = './tanghao_total.xlsx'
    xml_to_excel(path_of_cn=cn_p, path_of_en=en_p, excel_path=excel_path)


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

    for kce in list_kce:
        if len(kce.cn) > 0:
            cn_list.append(KCEBean(key=kce.key, cn=kce.cn, en=''))
        if len(kce.en) > 0:
            en_list.append(KCEBean(key=kce.key, cn='', en=kce.en))

    write_kce_to_path(list_of_kce=en_list, path=xml_path + 'kce_of_eng.xml', key='en')
    write_kce_to_path(list_of_kce=cn_list, path=xml_path + 'kce_of_ch.xml', key='cn')


if __name__ == "__main__":
    sys.exit(main())
