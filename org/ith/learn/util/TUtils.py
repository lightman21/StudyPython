import hashlib
import html
import os
import re
import time

import xlrd
import xlwt

from org.ith.learn.util.Colored import COLS
import random


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


def write_to_excel(to_write_list, path_of_excel):
    """
    将list_of_kec 写到指定指定路径
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
        list_kce = []
        rets = re.findall(fuzzy_matching, all_str)
        for ret in rets:
            if lang == 'cn':
                kce = KCEBean(key=ret[0], cn=ret[1], en='')
            else:
                kce = KCEBean(key=ret[0], en=ret[1], cn='')

            list_kce.append(kce)

        return list_kce


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


if __name__ == '__main__':
    print(extra_chinese('tanghao唐浩 fasdfj !_ '))
