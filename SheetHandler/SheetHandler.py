# -*- coding: utf-8 -*-
import xlrd
import os


class SheetHandler(object):
    index = {
        "stu_id": 0,
        "name_zh": 0,
        "time": 0
    }
    actinfo_list = list()

    def __init__(self, file_name):
        try:
            workbook = xlrd.open_workbook(filename=file_name)
            self.sheet = workbook.sheet_by_index(0)
        except:
            workbook = None
            self.sheet = None

    def resolve_sheet(self):
        sheet_title = self.sheet.row_values(0)
        self.index["name_zh"] = sheet_title.index("姓名")
        self.index["stu_id"] = sheet_title.index("学号")
        try:
            self.index["time"] = sheet_title.index("时长")
        except:
            self.index["time"] = sheet_title.index("志愿时长")
        return sheet_title.index

    def generate_info(self):
        rows = self.sheet.nrows
        for i in range(1,rows):
            info = {
                "stu_id": self.sheet.cell_value(i, self.index["stu_id"]),
                "name_zh": self.sheet.cell_value(i, self.index["name_zh"]),
                "time": self.sheet.cell_value(i, self.index["time"])
            }
            self.actinfo_list.append(info)
        print(self.actinfo_list)
        return self.actinfo_list
