import os
import re
from datetime import datetime

import fitz  # PyMuPDF
import pdfplumber
import re


def find_first_num(text):
    match = re.search(r'\d+(\.\d+)?', text)

    if match:
        first_number = match.group()
        print(f"找到的第一个数字是：{first_number}")
        return first_number
    else:
        print("没有找到数字。")


def find_second_num(text):
    pattern = r'\d+(\.\d+)?'
    match = re.search(pattern, text)
    if match:
        first_number = match.group()
        print(f"找到的第一个数字是：{first_number}")

        # 从第一个数字的末尾继续搜索下一个数字
        start_index = match.end()
        match = re.search(pattern, text[start_index:])

        if match:
            second_number = match.group()
            print(f"找到的第二个数字是：{second_number}")
            return second_number
        else:
            print("没有找到第二个数字。")
    else:
        print("没有找到数字。")


def pdf_read_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

    return text


def now_str():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y-%m-%d, %H:%M:%S")
    print("date and time:", date_time)
    return date_time

# 是否中文大写金额
def is_chinese_currency(text):
    pattern = re.compile(r"^(?:[零壹贰叁肆伍陆柒捌玖]|\d)+(?:[元角分])+$")
    return bool(pattern.match(text))

def contains_chinese_currency(text):
    pattern = re.compile(r"(?:[零壹贰叁肆伍陆柒捌玖]|\d)+(?:[元角分])")
    return bool(pattern.search(text))


def find_chinese_currency(text):
    pattern = r'[\u4e00-\u9fa5]+'

    chinese_amount = re.findall(pattern, text)
    rs = chinese_amount[0] if chinese_amount else None

    return rs

chinese_num = {
    u'〇': 0, u'零': 0,
    u'一': 1, u'壹': 1,
    u'二': 2, u'两': 2, u'贰': 2,
    u'三': 3, u'叁': 3,
    u'四': 4, u'肆': 4,
    u'五': 5, u'伍': 5,
    u'六': 6, u'陆': 6,
    u'七': 7, u'柒': 7,
    u'八': 8, u'捌': 8,
    u'九': 9, u'玖': 9,
    u'十': 10, u'拾': 10,
    u'百': 100, u'佰': 100,
    u'千': 1000, u'仟': 1000,
    u'万': 10000, u'萬': 10000,
    u'亿': 100000000, u'億': 100000000,
}


def chinese2digits(value):
    total = 0.00
    # 基础单位
    base_unit = 1
    # 可变单位
    dynamic_unit = 1
    for i in range(len(value) - 1, -1, -1):
        val = chinese_num.get(value[i])
        # 表示单位
        if val > 10:
            if val > base_unit:
                base_unit = val
            else:
                dynamic_unit = base_unit * val
        # 10既可以做单位也可做数字
        elif val == 10:
            if i == 0:
                if dynamic_unit > base_unit:
                    total = total + dynamic_unit * val
                else:
                    total = total + base_unit * val
            else:
                dynamic_unit = base_unit * val
        else:
            if dynamic_unit > base_unit:
                total = total + dynamic_unit * val
            else:
                total = total + base_unit * val
    return total