from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, KCEBean, highlight


# def excel_to_xml(path_of_excel, xml_path='../../../docs/'):
def excel_to_xml(path_of_excel, xml_path='./'):
    list_kce = open_excel_as_list(path_of_excel)
    cn_list = []
    en_list = []

    cn_hold_list = list()
    en_hold_dict = dict()

    print('path_of_excel:', path_of_excel)

    excel_name = path_of_excel.split('/')[-1].replace('.', '')

    import re
    pattern = r'\%[\d]\$[sd]'

    for kce in list_kce:
        if len(kce.cn) > 0:
            bean = KCEBean(key=kce.key, cn=kce.cn, en=kce.en)
            bean.en = ''
            cn_list.append(bean)
            ret = re.findall(pattern, str(bean.cn))
            if len(ret) > 0:
                cn_hold_list.append(bean)

        if len(kce.en) > 0:
            bean = KCEBean(key=kce.key, cn=kce.cn, en=kce.en)
            bean.cn = ''
            en_list.append(bean)
            en_hold_dict[bean.key] = bean.en

    err_count = 0
    for holder in cn_hold_list:
        if en_hold_dict.keys().__contains__(holder.key):
            cn_ret = re.findall(pattern, holder.cn)
            en_ret = re.findall(pattern, en_hold_dict[holder.key])
            cn_ret = sorted(cn_ret)
            en_ret = sorted(en_ret)
            if cn_ret != en_ret:
                print(highlight('cn is ', 2), holder.cn, highlight('but en is', 4), en_hold_dict[holder.key],
                      ",the key is ", highlight(holder.key))
                err_count += 1
    if err_count > 0:
        print("total cn count", highlight(len(cn_list), 3), ',the error en count ', highlight(err_count, 2))
    else:
        write_kce_to_path(en_list, xml_path + excel_name + ".xml", key='en')


def main(argv=None):
    print("the argv is ", argv)
    exel_path = '/Users/toutouhiroshidaiou/Desktop/0727___KMobile_Android_07_22.xlsx'
    out_path = '/Users/toutouhiroshidaiou/Desktop/'
    excel_to_xml(exel_path, out_path)
    pass


if __name__ == '__main__':
    main()
