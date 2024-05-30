#-*- coding:utf-8 -*-
import requests
import urllib3
import ssl


# 创建自定义适配器
class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.set_ciphers("RSA")
        context.maximum_version = ssl.TLSVersion.TLSv1_2

        context.options &= ssl.OP_NO_SSLv3
        context.options &= ssl.OP_NO_TLSv1_3

        kwargs['ssl_context'] = context
        kwargs['ssl_version'] = ssl.PROTOCOL_TLSv1
        return super().init_poolmanager(*args, **kwargs)


def request_new_tst(url):
    # 创建会话并使用自定义适配器
    session = requests.Session()
    session.mount('https://', TLSAdapter())
    # 发送请求
    response = session.get(url, verify=False)
    print(response.content)


url = "https://bcfp.shenzhen.chinatax.gov.cn/verify/scan?hash=01645d47765dd7aec052188019747d2b9ff4a734a5a7c45ffec86832c070910a19&bill_num=09826096&total_amount=96200"
request_new_tst(url)
