import sys

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, KCEBean, exec_cmd


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # path_excel = '/Users/toutouhiroshidaiou/Desktop/android_i18n_0407.xlsx'
    # excel_to_xml(path_excel)

    cmd = 'git archive --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git ' \
          'HEAD:app/src/main/res/values-en/ strings.xml | tar -x '

    exec_cmd(cmd)


def excel_to_xml(path_of_excel):
    list_kce = open_excel_as_list(path_of_excel)
    cn_list = []
    en_list = []

    for kce in list_kce:
        if len(kce.cn) > 0:
            cn_list.append(KCEBean(key=kce.key, cn=kce.cn, en=''))
        if len(kce.en) > 0:
            en_list.append(KCEBean(key=kce.key, cn='', en=kce.en))

    print('cn size ', len(cn_list), ',en size ', len(en_list))

    write_kce_to_path(list_of_kce=en_list, path='../../../docs/kce_en.xml', key='en')
    write_kce_to_path(list_of_kce=cn_list, path='../../../docs/kce_of_cn.xml', key='cn')

    pass


if __name__ == "__main__":
    sys.exit(main())
