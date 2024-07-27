import re

import fitz  # PyMuPDF
import pdfplumber


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
    rs = []
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        lines = page.extract_words()
        for line in lines:
            item = [
                line.get('x0'),
                line.get('top'),
                line.get('x1'),
                line.get('bottom'),
                line.get('text')
            ]
            print(item)
            rs.append(item)

    return rs


def is_number(text):
    try:
        float(text)
        print("The text is a float.")
    except ValueError:
        print("The text is not a number.")
        return False
    return True


def find_numbers(text):
    # 正则表达式匹配整数和小数
    pattern = r'\d+\.\d+'
    return re.findall(pattern, text)
