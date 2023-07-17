# https://tls.browserleaks.com/json
# https://tls.peet.ws/api/all
# 突破TLS/JA3指纹的方案

# pass 1
# #pip install curl_cffi   # https://github.com/yifeikong/curl_cffi
# from curl_cffi import requests
# # 注意 impersonate 这个参数
# r = requests.get("https://tls.browserleaks.com/json", impersonate="chrome101")
 
# print(r.json())
# # output: {'ja3_hash': '53ff64ddf993ca882b70e1c82af5da49'
# # 指纹和目标浏览器一致
 
# # 支持使用代理
# proxies = {"https": "http://localhost:3128"}
# r = requests.get("https://tls.browserleaks.com/json", impersonate="chrome101", proxies=proxies)
 
 
# from curl_cffi import Curl, CurlOpt
# from io import BytesIO
 
# buffer = BytesIO()
# c = Curl()
# c.setopt(CurlOpt.URL, b'https://tls.browserleaks.com/json')
# c.setopt(CurlOpt.WRITEDATA, buffer)
 
# c.impersonate("chrome101")
 
# c.perform()
# c.close()
# body = buffer.getvalue()
# print(body.decode())  # 查看当前请求的ja3信息



# pass 2
# #pip install tls-client   # https://github.com/FlorianREGAZ/Python-Tls-Client
# import tls_client
 
# # You can also use the following as `client_identifier`:
# # Chrome --> chrome_103, chrome_104, chrome_105, chrome_106, chrome_107, chrome_108, chrome109, Chrome110,
# #            chrome111, chrome112
# # Firefox --> firefox_102, firefox_104, firefox108, Firefox110
# # Opera --> opera_89, opera_90
# # Safari --> safari_15_3, safari_15_6_1, safari_16_0
# # iOS --> safari_ios_15_5, safari_ios_15_6, safari_ios_16_0
# # iPadOS --> safari_ios_15_6
# # Android --> okhttp4_android_7, okhttp4_android_8, okhttp4_android_9, okhttp4_android_10, okhttp4_android_11,
# #             okhttp4_android_12, okhttp4_android_13
 
# session = tls_client.Session(
#     client_identifier="chrome112",
#     random_tls_extension_order=True
# )
 
# res = session.get(
#     "https://www.example.com/",
#     headers={
#         "key1": "value1",
#     },
#     proxy="http://user:password@host:port"
# )


import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
 
ORIGIN_CIPHERS = ('ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
                  'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES')
 
 
class DESAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        """
        A TransportAdapter that re-enables 3DES support in Requests.
        """
        CIPHERS = ORIGIN_CIPHERS.split(':')
        random.shuffle(CIPHERS)
        CIPHERS = ':'.join(CIPHERS)
        self.CIPHERS = CIPHERS + ':!aNULL:!eNULL:!MD5'
        super().__init__(*args, **kwargs)
 
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)
 
    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)
 
 
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'}
s = requests.Session()
s.headers.update(headers)
 
for _ in range(5):
    s.mount('https://tls.browserleaks.com', DESAdapter())
    resp = s.get('https://tls.browserleaks.com/json').json()
    print(resp)