import os
import re
from datetime import datetime

import cn2an
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


def parse_chinese_amount(amount_str):
    """
    将中文金额字符串转换为数字
    """
    # 中文数字到阿拉伯数字的映射
    chinese_digits = {
        '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4,
        '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9
    }

    # 中文单位到阿拉伯单位的映射
    chinese_units = {
        '': 1, '十': 10, '百': 100, '千': 1000,
        '万': 10000, '亿': 100000000
    }

    total = 0
    unit = 1
    for char in reversed(amount_str):
        if char in chinese_digits:
            total += chinese_digits[char] * unit
        elif char in chinese_units:
            unit *= chinese_units[char]
        elif char == '点':
            unit = 1

    return total




