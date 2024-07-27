import os
from decimal import Decimal

import cv2  # opencv包

import requests
import ssl

import util
from util import pdf_read_text

ssl._create_default_https_context = ssl._create_unverified_context

import consts


def do_parse(pdf_path):
    img_path = util.pdf_to_img(pdf_path)
    info = read_qr_code(img_path)

    os.remove(img_path)

    parse_pdf(pdf_path, info)
    return info


def read_qr_code(img_path):
    """
    读取图片中的二维码
    :param img_path:图片路径
    :type img_path:str
    :return:识别的内容
    :rtype:tuple
    """
    detector = cv2.wechat_qrcode_WeChatQRCode()  # 微信贡献的代码，很好用
    img = cv2.imread(img_path)
    if img is None:
        return {"sys_msg": '没有二维码'}  # 没有二维码
    res, _ = detector.detectAndDecode(img)
    if res is None or len(res) == 0:
        return {"sys_msg”:“解析二维码为空"}

    # 深圳电子发票
    if res[0].startswith("https://bcfp.shenzhen.chinatax.gov.cn"):
        url = res[0]
        print(url)

        return parse_shenzhen(url)

    res = res[0].split(',')
    if res[0] != '01':  # 第1个属性值，固定01
        raise ValueError("发票二维码第一个应该是固定01")
    info = {
        "发票类型": res[1],  # 发票种类代码
        "发票代码": res[2],
        "发票号码": res[3],
        "发票金额": Decimal(res[4]),
        "开票日期": res[5],
        "校验码": res[6],
    }

    info['发票类型_中文'] = consts.INV_TYPE_DICT.get(info['发票类型'])

    return info


def parse_pdf(pdf_path, info):
    print('开始解析' + pdf_path)
    print(info)
    text = pdf_read_text(pdf_path)
    arr = text.split('\n')

    for item in arr:
        # '贰拾肆圆零柒分 ¥24.07'
        chinese_currency = util.contains_chinese_currency(item)
        if chinese_currency:
            print("解析到中文大写:", item)
            arr = item.split(' ')
            print('空格分割', len(arr))
            for a in arr:
                rs = util.find_chinese_currency(a)
                if rs:
                    info['价税合计_大写'] = rs
                    info['价税合计'] = Decimal(util.chinese_to_numerals(rs))
                    info['税额'] = info['价税合计'] - info['发票金额']
                    break


def parse_shenzhen(url):
    print('requests版本', requests.__version__)

    # 发送请求
    response = requests.get(url)

    print(response.text)
    return {"sys_msg": "深圳发票解析"}


if __name__ == '__main__':
    url = "https://bcfp.shenzhen.chinatax.gov.cn/verify/scan?hash=01645d47765dd7aec052188019747d2b9ff4a734a5a7c45ffec86832c070910a19&bill_num=09826096&total_amount=96200"
    #   url = "https://www.baidu.com"
    parse_shenzhen(url)
