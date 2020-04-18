import os

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight


def main():
    path_535 = '/Users/lightman_mac/Desktop/0418work/535_app-official-armeabi-v7a-envSingapore/res/values/strings.xml'
    # from merged
    # path_535 = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res/merged/official/envSingapore/values/values.xml'
    path_535 = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/incremental/mergeOfficialEnvCiTestResources/merged.dir/values/values.xml'
    kce_list_535 = read_xml_as_kce_list(path_535)

    path_534 = '/Users/lightman_mac/Desktop/0418work/534app-official-armeabi-v7a-envCiTest/res/values/strings.xml'
    # from merged
    # path_534 = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/incremental/mergeOfficialEnvCiTestResources/merged.dir/values/values.xml'
    kce_list_old = read_xml_as_kce_list(path_534)

    key_olds = []
    for kce in kce_list_old:
        key_olds.append(kce.key)

    key_news = []
    for kce in kce_list_535:
        key_news.append(kce.key)

    diff_kce = []
    count = 0
    for new in kce_list_535:
        if new.key not in key_olds:
            if not str(new.key).__contains__('autogen'):
                if not str(new.key).__contains__('takeout_'):
                    if not str(new.key).__contains__('leak_canary_'):
                        print(new)
                        count += 1
                        diff_kce.append(new)

    print('534 len ', len(kce_list_old), ',535 len ', len(kce_list_535))
    print(', diff count ', count)
    write_kce_to_path(diff_kce, './diff_534_535.xml')


pass

if __name__ == '__main__':
    main()
