from org.ith.learn.OhMyEXCEL import excel_to_xml
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list

"""
git archive i18n_5.34.10 --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git app/src/main/res/values-en/strings.xml | tar -x

"""


def main():
    # path_of_xml = '/Users/toutouhiroshidaiou/Desktop/i18n/'
    # ret = excel_to_xml('/Users/toutouhiroshidaiou/Desktop/i18n/413_i18n_android.xlsx', xml_path=path_of_xml)
    # # cn_out_path, en_out_path
    # en_path = ret[1]
    # en_kce_list = read_xml_as_kce_list(en_path)
    # for enk in en_kce_list:
    #     enk.cn = auto_escape(enk.cn)

    remote_xml = '/tmp/remote.xml'
    remote_list = read_xml_as_kce_list(remote_xml)

    new_xml = './shuangwei413.xml'
    new_list = read_xml_as_kce_list(new_xml)

    print('remote size ', len(remote_list), ', new size ', len(new_list))

    diff_list = []

    remote_keys = []
    new_keys = []

    for key in remote_list:
        remote_keys.append(key.key)

    for key in new_list:
        new_keys.append(key.key)

    # for new in new_list:

    count = 0
    diff_list = []
    # 计算new 比remote多出来的
    for new in new_list:
        if new.key not in remote_keys:
            diff_list.append(new)
            print(new)
            count += 1

    write_kce_to_path(diff_list, 'tmp/diff_remote.xml')

    modify_list = []

    for kce in remote_list:
        for new in new_list:
            if kce.key == new.key:
                if kce.cn != new.cn:
                    print(kce.key, ', new.cn ' + new.cn + ', remote.cn ' + kce.cn)
                    modify_list.append(new)

    write_kce_to_path(modify_list, 'tmp/modify_list.xml')

    print('diff size ', count)


if __name__ == '__main__':
    main()
