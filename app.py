import json
import os
import sys
import time
import traceback
from decimal import Decimal

from flask import Flask, request, render_template

import parse

app = Flask(__name__, static_url_path="")
app.secret_key = 'zhrmghgws'
app.json.ensure_ascii = False  # 解决中文乱码问题


@app.route('/')
def home():
    python_version = sys.version
    return render_template("index.html", python_version=python_version)


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("files")
    rs = []
    for file in files:
        pdf_path = "uploads/" + str(time.time())
        file.save(pdf_path)

        info = {'文件名': file.filename}

        try:
            parse.do_parse(pdf_path, info)
        except Exception as e:
            print('解析发票异常', e)
            traceback.print_exc()

            info['状态'] = str(e)

        print("正在删除文件", pdf_path)
        os.remove(pdf_path)

        # decimal 转 str, 否则json报错
        info = {key: str(value) if isinstance(value, Decimal) else value for key, value in info.items()}
        print("文件解析结果：", info)

        rs.append(info)

    print(rs)

    python_version = sys.version
    print("python 版本", python_version)

    cols = ("文件名",
            "发票标题",
            "发票代码", "发票号码", "开票日期", "校验码",
            "发票金额",
            "税额", "价税合计", "税率",
            "状态")

    print("开始渲染页面")

    return render_template("result.html",
                           list=rs,
                           cols=json.dumps(cols, ensure_ascii=False),
                           data=json.dumps(rs, ensure_ascii=False),
                           python_version=python_version
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
