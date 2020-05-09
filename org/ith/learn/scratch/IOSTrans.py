import re

from org.ith.learn.util.TUtils import KCEBean, md5, \
    auto_escape, remove_punctuation, exec_cmd, sort_dict_as_list

relative_dir = '../../../../docs/i18n/'
ios_dict_path = relative_dir + 'ios_kce_dict.xml'


def main():
    gener_ios_dict(pull_ios_trans())


def gener_ios_dict(ios_kce_list):
    """
    自动拉取ios工程的develop分支 上的OnMobile/Resource/en.lproj/OnMobileLocalizable.strings文件
    并生成ios_kce_dict文件
    """
    to_write_lines = []
    kv_dict = dict()
    for kce in ios_kce_list:
        kv_dict[kce.cn] = kce.en

    kv_dict = sort_dict_as_list(kv_dict)

    ios_kce_list.clear()
    for kv in kv_dict:
        bean = KCEBean(key=md5(kv[0]), cn=kv[0], en=kv[1])
        ios_kce_list.append(bean)

    for kce in ios_kce_list:
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            v_cn = auto_escape(kce.cn).strip()
            v_en = auto_escape(kce.en).strip()
            line = '<kce key="{}" cn="{}" en="{}"/>\n'.format(kce.key, v_cn, v_en)
            to_write_lines.append(line)

    with open(ios_dict_path, 'w') as out:
        out.writelines(to_write_lines)


def pull_ios_trans():
    command = 'git archive develop --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile.git  ' \
              'OnMobile/Resource/en.lproj/OnMobileLocalizable.strings | tar -x && cp ' \
              'OnMobile/Resource/en.lproj/OnMobileLocalizable.strings ../../../../docs/i18n/ && rm -rf OnMobile '
    exec_cmd(command)
    return read_ios_as_kce(relative_dir + 'OnMobileLocalizable.strings')


def read_ios_as_kce(path):
    pattern = r'"(.*)" = "(.*)"'
    kce_list = []
    with open(path, 'r') as rin:
        content = rin.read()
        rets = re.findall(pattern, content)
        for ret in rets:
            b = KCEBean(key=md5(ret[0]), cn=remove_punctuation(auto_escape(ret[0])),
                        en=remove_punctuation(auto_escape(ret[1])))
            kce_list.append(b)
    return kce_list


if __name__ == '__main__':
    main()
