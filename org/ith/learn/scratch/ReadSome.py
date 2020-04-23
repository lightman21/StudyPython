from org.ith.learn.OhMyEXCEL import gener_cn_en_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import read_xml_as_kce_list, write_to_excel


def demo():
    path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res/merged' \
           '/official/envCiTest/values/values.xml '
    new_list_kce = read_xml_as_kce_list(path.strip())
    print(len(new_list_kce))

    old_path = '/Users/lightman_mac/Desktop/0411work/tsd/tanghao_0407xlsx_china.xml'
    old_list_kce = read_xml_as_kce_list(old_path.strip())

    old_keys = []
    for old in old_list_kce:
        old_keys.append(old.key)

    diff_list = []
    for new_kce in new_list_kce:
        if new_kce.key not in old_keys:
            if not str(new_kce.key).startswith('abc_'):
                diff_list.append(new_kce)

    ce_dict = gener_cn_en_dict('/Users/lightman_mac/Desktop/0411work/panshuangwei_0410_origin.xlsx')

    count = 0
    for kce in diff_list:
        if ce_dict.get(kce.cn):
            kce.en = ce_dict.get(kce.cn)
            count += 1
        else:
            print(kce)

    print('before trans size ', len(diff_list), ',transed ' + str(count))


if __name__ == '__main__':
    # # 比较输入的两个xml
    # i18n_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values-en/strings.xml'
    # master_path = '/Users/lightman_mac/Desktop/0411work/04112328master/en_strings.xml'
    #
    # i18_list = read_xml_as_kce_list(i18n_path)
    # master_list = read_xml_as_kce_list(master_path)
    #
    # i18keys = []
    # for i18 in i18_list:
    #     i18keys.append(i18.key)
    #
    # masterkeys = []
    # for master in master_list:
    #     masterkeys.append(master.key)
    #
    # for m in masterkeys:
    #     if m not in i18keys:
    #         print('in master but no in i18n ', m)
    #
    # print('i18 size ', len(i18_list), ',master size ', len(master_list))

    # master的key是不是都在i18n中

    path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values/strings.xml'
    kce_list = read_xml_as_kce_list(path)
    for kce in kce_list:
        if kce.key == 'takeout_sales_return_thirdorder_create_operation':
            print(kce)

    write_to_excel(kce_list, './shit.xlsx')
