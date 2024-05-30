import base64
import json
import sys
import time
from decimal import Decimal

from flask import Flask, request, render_template

import parse
import parse_pdf
from consts import INV_KEYS

app = Flask(__name__, static_url_path="")
app.secret_key = 'zhrmghgws'
app.json.ensure_ascii = False  # 解决中文乱码问题


@app.route('/')
def home():
    ip = request.remote_addr
    print('请求首页', ip)
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("files")
    list = []
    for file in files:
        pdf_path = "uploads/" + str(time.time())
        file.save(pdf_path)

        file_path = parse.pdf_to_img(pdf_path)
        info = parse.read_qr_code(file_path)
        parse_pdf.parse_pdf(pdf_path, info)

        info['文件名称'] = file.filename

        # decimal 转 str, 否则json报错
        info = {key: str(value) if isinstance(value, Decimal) else value for key, value in info.items()}

        list.append(info)

    print(list)

    python_version = sys.version

    return render_template("result.html",
                           list=list,
                           cols=json.dumps(INV_KEYS, ensure_ascii=False),
                           data=json.dumps(list, ensure_ascii=False),
                           python_version=python_version
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
