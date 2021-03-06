import html

import xlrd
import xlwt


class KCEBean:
    def __init__(self, key, cn, en):
        self.key = key
        self.cn = cn
        self.en = en

    def __str__(self):
        return "key: " + str(self.key) + "\tcn: " + str(self.cn) + "\ten: " + str(self.en)

    def __lt__(self, other):
        return self.key.lower() < other.key.lower()


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
    worksheet = workbook.add_sheet('sheet_of_kce')
    worksheet.write(0, 0, "key")
    worksheet.write(0, 1, "cn")
    worksheet.write(0, 2, "en")

    for row, item in enumerate(to_write_list):
        for column in range(3):
            key = item.key
            cn = item.cn
            en = item.en
            row += 1
            if column == 0:
                worksheet.write(row, column, key)
            elif column == 1:
                worksheet.write(row, column, cn)
            else:
                worksheet.write(row, column, en)

    workbook.save(path_of_excel)

    print(path_of_excel + " write done.")


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
