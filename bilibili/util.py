# -*-coding:utf-8 -*-
# 参考https://github.com/Vespa314/bilibili-api/blob/master/api.md
import re
import json
import time
import zlib
import hashlib
import urllib.request
from urllib.parse import quote
from urllib.error import HTTPError


class JsonInfo:
    """请求指定Api地址获取JSON响应，然后处理为Python对象"""
    json = None  # json转换为Python的dict对象
    error = False  # 是否出错
    error_msg = ""  # 错误信息

    def __init__(self, url, pre_deal=lambda x: x):
        """
        将网址信息解析为json格式
        :param url: 网址
        :param pre_deal: 预处理函数
        """
        """
        json.loads(s, *, encoding=None,...)
        使用转换表反序列化s（一个str，bytes或者含有JSON文档的bytearray实例）为Python对象dict。
        要使用自定义JSONDecoder子类，请使用cls kwarg指定它; 否则使用JSONDecoder。其他关键字参数将传递给类的构造函数。
        如果要反序列化的数据不是有效的JSON文档， 则会引发JSONDecodeError。输入编码应为UTF-8，UTF-16或UTF-32。
        """
        self.json = json.loads(pre_deal(get_url_content(url)))

        if 'code' in self.json.keys() and self.json['code'] != 0:
            if 'message' in self.json.keys():
                self.error_msg = self.get_value('message')
            elif 'error' in self.json.keys():
                self.error_msg = self.get_value('error')
            self.error = True

    def get_value(self, *keys):
        """
        获取多级dict的值
        :param keys: 键，第一个参数是第一级的键，第二个参数是第二级的键，依次类推
        :return: 值
        """
        count = len(keys)
        if count == 0:
            return None

        temp = self.json
        i = 0
        while i < count:
            if type(temp) == dict and keys[i] in temp.keys():
                temp = temp[keys[i]]
                i = i + 1
            else:
                return None
        return temp


def get_url_content(url, headers=None):
    """
    根据所给地址请求并返回网页信息
    :param url: 网址
    :param headers: 自定义请求头
    :return: string 网页信息
    """
    page = ""
    content = ""
    if not headers:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }

    try:
        request = urllib.request.Request(url=url, headers=headers)
        page = urllib.request.urlopen(request)
        content = page.read()
    except HTTPError as e:
        if e.code == 404:
            return ""
        else:
            exit(e)
    except Exception as e:
        exit(e)

    if page.info().get('Content-Encoding') == 'gzip':  # info()返回页面头信息字典
        """
        zlib.decompress(string[, wbits[, bufsize]])
        解压缩字符串数据，返回包含未压缩数据的字符串。
        wbits参数取决于字符串格式。
        如果给出bufsize，则将其用作输出缓冲区的初始大小。
        如果发生任何错误，则引发异常error。

        该wbits参数控制历史缓冲区的大小（或“窗口大小”），头部和尾部的格式是预先定好的。
        它类似于compressobj()参数，但接受更多范围的值：
        +8到+15：基于2的对数的窗口大小。输入必须包含zlib头部和尾部。
        0：从zlib头部自动确定窗口大小。仅自zlib 1.2.3.5起支持。
        -8到-15：使用wbits的绝对值作为窗口大小的对数。输入必须是没有头部和尾部的原始数据流。
        +24到+31 = 16 +（8到15）：使用该值的低4位作为窗口大小对数。输入必须包含gzip头部和尾部。
        +40到+47 = 32 +（8到15）：使用该值的低4位作为窗口大小对数，并自动接受zlib或gzip格式。

        解压缩流时，窗口大小不得小于最初用于压缩流的大小; 使用太小的值可能会导致error异常。
        默认的wbits值为15，这对应于最大窗口大小（zlib.MAX_WBITS），并且需要包含zlib头部和尾部。

        bufsize是用于保存解压缩数据的缓冲区的初始大小。
        如果需要更多空间，缓冲区大小将根据需要增加，因此您不必完全正确地获取此值; 
        调整它只会节省几个malloc()调用。默认大小为16384。
        """
        content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
        # content = str(content, encoding='utf-8')
    return content


def get_json_info(url):
    json_info = JsonInfo(url)
    if json_info.error:
        exit(json_info.error_msg)
    else:
        return json_info


def get_re(regexp, content):
    return re.findall(regexp, content)


def get_keyword(keyword):
    """
    解决中文url地址的转码问题
    urllib.parse.quote(string, safe='/', encoding=None, errors=None)
    使用转义%xx替换字符串中的特殊字符。
    不会替换字母，数字和字符'_.-~'。
    默认情况下，此函数用于转义URL的路径部分。
    string可以是str或bytes。
    可选的safe参数指定不应转义的其他ASCII字符 - 其默认值为'/'。
    可选的encoding和errors参数指定如何处理str.encode()方法所接受的非ASCII字符。 编码默认为'utf-8'。
    错误默认为'strict'，意味着不支持的字符引发 UnicodeEncodeError。
    如果string是bytes，则不得提供encoding和errors，否则会引发一个TypeError。
    """
    return quote(keyword)


def get_search_string(params):
    if type(params) != dict or params == {}:
        return ""

    string = ""
    paras = params.keys()
    for para in paras:
        if string != "":
            string += "&"
        string += para + "=" + str(params[para])


def get_sign(params: dict, app_key='84956560bc028eb7', app_secret='94aba54af9065f71de72f5508f1cd42e'):
    params['appkey'] = app_key
    data = ""
    paras = sorted(params)
    for para in paras:
        if data != "":
            data += "&"
        data += para + "=" + str(params[para])
    if not app_secret:
        return data

    m = hashlib.md5()
    m.update(str(data + app_secret).encode('utf-8'))
    return data + '&sign=' + m.hexdigest()


def exec_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print('共耗时：{} 秒'.format(time.time() - start_time))
        return result

    return wrapper
