import os
from decimal import Decimal

import fitz  # PyMuPDF

import cv2  # opencv包

import consts
from parse_pdf import parse_pdf


def pdf_to_img(file_path):
    # 打开PDF文件
    pdf_document = fitz.open(file_path)

    page = pdf_document[0]

    rotate = int(0)
    zoom_x = 1.33333333
    zoom_y = 1.33333333
    mat = fitz.Matrix(zoom_x, zoom_y)
    mat = mat.prerotate(rotate)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    temp_img_path = file_path + '.temp.png'
    pix.save(temp_img_path)
    pdf_document.close()

    return temp_img_path



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
        return None  # 没有二维码
    res, _ = detector.detectAndDecode(img)
    if res is None or len(res) == 0:
        return None
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

    info['发票类型_中文'] = consts.INV_TYPE_DICT.get( info['发票类型'])

    return info



