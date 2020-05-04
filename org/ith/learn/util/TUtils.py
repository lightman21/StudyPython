import collections
import hashlib
import html
import os
import re
import sys
import time
import xml

import xlrd
import xlwt

from org.ith.learn.util.Colored import COLS
import random

"""
git archive i18n_5.34.10 --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git app/src/main/res/values-en/strings.xml | tar -x

"""


class KCEBean:
    def __init__(self, key, cn, en):
        self.key = key
        self.cn = cn
        self.en = en

    def hl(self):
        hkey = highlight('key:', 2)
        hcn = highlight('cn:', 3)
        hen = highlight('en:', 4)
        result = '{} {:<30} {} {:<20} {} {:<20}'.format(hkey, str(self.key), hcn, str(self.cn), hen, str(self.en))
        return result

    def __str__(self):
        # return 'key:{:<30} cn:{:<20} en:{:<20}'.format(str(self.key), str(self.cn), str(self.en))
        return 'key:{}___cn:{}___en:{}'.format(str(self.key), str(self.cn), str(self.en))

    def __lt__(self, other):
        return self.key.lower() < other.key.lower()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # return self.key == other.key and self.cn == other.cn and self.en == other.en
            return self.key == other.key and self.cn == other.cn

    def __hash__(self):
        return hash(self.key)


class XmlStdin:
    def __init__(self):
        self.str = ""

    def write(self, value):
        self.str += value

    def toString(self):
        txt = html.unescape(self.str)
        return txt


def do_search_dict(kce_list):
    cn_en_dict = dict()
    for kce in kce_list:
        if cn_en_dict.get(kce.cn) is None:
            cn_en_dict[kce.cn] = kce.en
    count = 0
    for kce in kce_list:
        if len(kce.en) == 0 and len(kce.cn) != 0:
            # 有中文没有英文  查一下表
            in_dict = cn_en_dict.get(kce.cn)
            if in_dict is not None and len(in_dict) > 0:
                # 查表有值
                kce.en = in_dict
                print(highlight('do_search_dict ', 2), kce.hl())
                count += 1

    print(highlight('do search dict count '), count)

    return kce_list


def write_to_excel(to_write_list, path_of_excel):
    # 处理一下 中英文的情况
    dict_kce_list = do_search_dict(to_write_list)
    now_date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    out = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/docs/dicts/by_dict/' + now_date
    twrite_kce_to_path(dict_kce_list, key='cn', path=out + '__china.xml')
    twrite_kce_to_path(dict_kce_list, key='en', path=out + '__english.xml')

    """
    将list_of_kce 写到指定指定路径
    """
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Android_i18n')
    worksheet.write(0, 0, "key")
    worksheet.write(0, 1, "中文")
    worksheet.write(0, 2, "英文")

    for row, item in enumerate(to_write_list):

        row += 1

        for column in range(3):
            key = item.key
            cn = item.cn
            en = item.en

            if column == 0:
                worksheet.write(row, column, key)
            elif column == 1:
                worksheet.write(row, column, cn)
            else:
                worksheet.write(row, column, en)

            # row += 1

    workbook.save(path_of_excel)

    print(highlight(path_of_excel + " write done."))


def open_excel_as_list(file_path):
    data = xlrd.open_workbook(file_path)
    sheets = data.sheets()
    list_keys = []
    list_china = []
    list_english = []
    # key cn en
    sheet = sheets[0]

    cols_count = sheet.ncols

    is_one_column = cols_count == 1
    is_two_column = cols_count > 2 and (len(sheet.col(2)[0].value) == 0)
    is_three_column = cols_count > 2 and (len(sheet.col(2)[0].value) != 0)

    rg = 3 if is_three_column else 2 if is_two_column else 1

    for col in range(rg):
        # read three clumn key cn en
        if is_three_column:
            if col == 0:
                list_keys = sheet.col(col)
            elif col == 1:
                list_china = sheet.col(col)
            else:
                list_english = sheet.col(col)
        elif is_one_column:
            if col == 0:
                list_china = sheet.col(col)
        elif is_two_column:
            if col == 0:
                list_china = sheet.col(col)
            elif col == 1:
                list_english = sheet.col(col)

    list_kces = []

    for i in range(len(list_china)):
        if is_one_column:
            list_kces.append(KCEBean("", list_china[i].value, ""))
        if is_two_column:
            list_kces.append(KCEBean("", list_china[i].value, list_english[i].value))
        if is_three_column:
            list_kces.append(KCEBean(list_keys[i].value, list_china[i].value, list_english[i].value))

    return list_kces


def highlight(str_line, index=-1):
    CRED = '\033[93m'
    CEND = '\033[0m'
    if 0 <= index < len(COLS):
        CRED = COLS[index]
    else:
        CRED = random.choice(COLS)

    return '{} {} {}'.format(CRED, str_line, CEND)


def exec_cmd(cmd_str, cmd_log=True):
    r = os.popen(cmd_str)
    text = r.read()
    if cmd_log:
        print("execute command:", highlight(cmd_str), "\nresult:\n", text)
    r.close()
    return text


def modify_time(path_file):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(path_file).st_mtime))


def modify_timestamp(path_file):
    return os.stat(path_file).st_mtime


def remove_punctuation(s):
    return re.sub(r'[^\w\s]', '', s)


def read_xml_as_kce_list(xml_path, lang='cn'):
    xml_path = xml_path.strip()
    with open(xml_path, 'r') as file:
        all_str = file.read()
        fuzzy_matching = r'<string name="(\w*)">(.*)</string>'
        fuzzy_matching = r'<string name="(\w*)">(.*?)</string>'
        # r = re.compile(matching, re.DOTALL)
        # rets = r.findall(mock_all_xml)
        # r = re.compile(fuzzy_matching, re.DOTALL)
        list_kce = []
        rets = re.findall(fuzzy_matching, all_str, re.DOTALL)
        # rets = r.findall(all_str)
        for ret in rets:
            if lang == 'cn':
                kce = KCEBean(key=ret[0], cn=ret[1], en='')
            else:
                kce = KCEBean(key=ret[0], en=ret[1], cn='')

            list_kce.append(kce)

        return list_kce


def gener_dict_by_path(xml_path):
    """
    读取指定xml_path路径下的文件
    生成一个dict
    dict中key为string-array,value为各个item值的元组
    """
    DOMTree = xml.dom.minidom.parse(xml_path)
    collection = DOMTree.documentElement
    string_arrays = collection.getElementsByTagName("string-array")

    value_tag_dict = dict()

    for str_arr in string_arrays:
        tag_name = str_arr.getAttribute('name')
        items = str_arr.getElementsByTagName('item')
        item_texts = list()
        for item in items:
            text = item.childNodes[0].data
            item_texts.append(text)
        value_tag_dict[tag_name] = tuple(item_texts)

    return value_tag_dict


def extract_string_array(xml_path, extract_path=''):
    return generate_string_array_xml_doc(gener_dict_by_path(xml_path), out_path=extract_path)


def generate_string_array_xml_doc(key_values_dict, out_path=''):
    """
    @param key_values_dict key为string-array的name,value为各个item的值的元组
    @param out_path 生成的xml的路径

    使用minidom生成XML
    0.创建Element,createElement
    1.添加子节点,appendChild
    2.创建Text,createTextNode
    3.创建属性,createAttribute
    """
    if len(key_values_dict) < 1:
        return

    print(highlight('key_values_dict len ', 3), len(key_values_dict))

    xml_header = '<?xml version="1.0" encoding="utf-8"?>\n'

    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'resources', None)
    resources_root = dom.documentElement

    # key 倒序
    key_values_dict = collections.OrderedDict(sorted(key_values_dict.items(), reverse=True, key=lambda t: t[0]))

    for key, values in key_values_dict.items():
        title = dom.createElement("string-array")
        title.setAttribute("name", key)
        for text_value in values:
            item = dom.createElement('item')
            item.appendChild(dom.createTextNode(text_value))
            title.appendChild(item)

        resources_root.appendChild(title)

    raw_string = resources_root.toprettyxml(indent="\t", newl='\n')

    if len(out_path) < 1:
        log_str = raw_string \
            .replace('</string-array>', '</string-array>\n') \
            .replace('<resources>', '') \
            .replace('</resources>', '')
        print(highlight(log_str, 4))
        return log_str
    else:
        # 有输出路径
        with open(out_path, 'w') as out:
            out.write(raw_string)

        with open(out_path, 'r') as rin:
            lines = rin.readlines()
            lines.insert(0, xml_header)
            tweaked_lines = []
            for line in lines:
                line = line.replace('</string-array>', '</string-array>\n')
                tweaked_lines.append(line)
            with open(out_path, 'w') as rout:
                rout.writelines(tweaked_lines)


def auto_transascii10(str_input):
    """
    把输入的软换行换成硬换行
    \n        10        换行NL
    \r        13        回车CR
    """
    ascii_indexes = []
    next_line_ascii = 10
    for index in range(len(str_input)):
        if ord(str_input[index]) == next_line_ascii:
            ascii_indexes.append(index)
    blank = list(str_input)
    for ch_index in ascii_indexes:
        blank[ch_index] = r'\n'

    return ''.join(blank)


def md5(str_data):
    return hashlib.md5(str_data.encode(encoding='UTF-8')).hexdigest()


def get_cur_branch():
    ret = exec_cmd("git branch | grep \\* | awk '{print$2}'")
    return ret.strip()


def is_contains_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def extra_chinese(word):
    outer = ''
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            outer += ch
    return outer


def auto_escape(inputing):
    """
    检查传入的字符串 是不是需要转义加\
    如果包含' 但是不包含\'
    则需要把' 替换伟\'
    """
    origin = ['\'', ]
    escape = ['\\\'', ]

    if len(inputing) > 0:
        for index in range(len(escape)):
            str_input = str(inputing)
            if str_input.__contains__(origin[index]):
                if not str_input.__contains__(escape[index]):
                    inputing = str_input.replace(origin[index], escape[index])
    return inputing


def twrite_kce_to_path(list_of_kce, path, sort=False, key='cn'):
    print('write_kce_to_path: ', highlight(path, 1))

    for kce in list_of_kce:
        kce.cn = auto_escape(kce.cn)
        kce.en = auto_escape(kce.en)

    list_of_kce = sorted(list_of_kce)

    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'resources', None)
    resources_root = dom.documentElement
    try:
        for kce in list_of_kce:
            string_node = dom.createElement('string')
            string_node.setAttribute("name", str(kce.key))
            str_key_value = str(kce.cn)
            if key != 'cn':
                str_key_value = str(kce.en)
            value = dom.createTextNode(str_key_value)
            string_node.appendChild(value)
            resources_root.appendChild(string_node)

        txmlstdin = XmlStdin()
        sys.stdin = txmlstdin
        dom.writexml(sys.stdin, addindent='\t', newl='\n', encoding='utf-8')
        transed_str = txmlstdin.toString()

        if not os.path.exists(path):
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

        with open(path, 'w') as f:
            f.write(transed_str)

        if not sort:
            return

        lines = list()
        with open(path, 'r') as f:
            for line in f:
                lines.append(line)
        lines = sorted(lines)
        last = lines[len(lines) - 2:]
        lines.insert(0, last[0])
        lines.insert(1, last[1])
        lines = lines[:- 2]
        outer = ''
        for line in lines:
            outer += line
        with open(path, 'w') as f:
            f.write(outer)

    except Exception as err:
        print("==================", path, err)
        raise


if __name__ == '__main__':
    print(remove_punctuation('税  !@#$%^&*( 种:'.replace(' ', '')))
