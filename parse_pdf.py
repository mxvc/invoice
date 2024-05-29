import util
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
            info['总金额_大写'] = rs
            info['总金额'] = util.chinese_to_numerals(rs)
            info['税额'] = info['总金额'] - info['金额_']
