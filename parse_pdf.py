import json

import fitz  # PyMuPDF
import re

import util
from parse_pdf_10 import parse_pdf_10
from parse_pdf_31 import parse_pdf_31
from util import pdf_read_text


def parse_pdf(pdf_path, info):
    print('开始解析' + pdf_path)
    print(info)
    text = pdf_read_text(pdf_path)
    arr = text.split('\n')

    for item in arr:
        # '贰拾肆圆零柒分 ¥24.07'
        if util.contains_chinese_currency(item):
            rs = util.find_chinese_currency(item)
            item['总金额_大写'] = rs
            item['总金额'] = util.chinese2digits(rs)






if __name__ == '__main__':
    text = pdf_read_text("D:/OneDrive/当前-发票/ERR_1.pdf")
    arr = text.split('\n')

    for item in arr:
        # '贰拾肆圆零柒分 ¥24.07'
        if util.contains_chinese_currency(item):
            rs = util.find_chinese_currency(item)

            print(item)
    print(text)
