# -*- coding: utf-8 -*-
import os
import sys
import threading
import traceback
import json
import urllib.parse

import akshare as ak
from flask import Flask, request
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.config['JSON_AS_ASCII'] = False
# webservice 欢迎页面

# 判断是否是下划线开头和结尾


def is_surrounded_by_underscores(text):
    return text.startswith('_') and text.endswith('_')


@app.route('/')
def index():
    interface_list = dir(ak)
    str1 = ''
    for interface in interface_list:
        if is_surrounded_by_underscores(str(interface)):
            continue
        str1 += str(interface)
        str1 += '<br/>'
        url1 = 'http://127.0.0.1:38080/api/public/'+str(interface)
        str1 += "<a href='{}'>{}</a>".format(url1, url1)
        str1 += '<br/>'
        str1 += str(eval('ak.'+interface+'.__doc__'))
        str1 += '<br/>'
        str1 += '<hr/>'
    str1 = str1.replace('\n', ' <br/> ')
    return """<!DOCTYPE html>
            <body>
                <h1>Ak Service Running!</h1>
                {}
            </body>
    """.format(str1)


def dict_to_func_args(param_dict):
    args = []
    for k, v in param_dict.items():
        args.append(f"{k}='{v}'")
    return ", ".join(args)


@app.route("/api/public/<item_id>")
def public(item_id: str):
    """
    接收请求参数及接口名称并返回 JSON 数据
    此处由于 AKShare 的请求中是同步模式，所以这边在定义 root 函数中没有使用 asyncio 来定义，这样可以开启多线程访问
    :param request: 请求信息
    :type request: Request
    :param item_id: 必选参数; 测试接口名 stock_dxsyl_em 来获取 打新收益率 数据
    :type item_id: str
    :return: 指定 接口名称 和 参数 的数据
    :rtype: json
    """
    interface_list = dir(ak)
    decode_params = urllib.parse.unquote(str(request.query_string))
    if item_id not in interface_list:
        return {
            "error": "未找到该接口，请升级 AKShare 到最新版本并在文档中确认该接口的使用方式：https://www.akshare.xyz"
        }, 404
    eval_str = dict_to_func_args(request.args)
    if not bool(request.args):
        try:
            print("excute: "+"ak." + item_id + f"()")
            received_df = eval("ak." + item_id + f"()")
            if received_df is None:
                return {
                    "error": "该接口返回数据为空，请确认参数是否正确：https://www.akshare.xyz"}, 404
            temp_df = received_df.to_json(orient="records", date_format="iso")
        except KeyError as e:
            return {
                "error": f"请输入正确的参数错误 {e}，请升级 AKShare 到最新版本并在文档中确认该接口的使用方式：https://www.akshare.xyz"
            }, 404
        return json.loads(temp_df)
    else:
        try:
            received_df = eval("ak." + item_id + f"({eval_str})")
            if received_df is None:
                return {"error": "该接口返回数据为空，请确认参数是否正确：https://www.akshare.xyz"}, 404
            temp_df = received_df.to_json(orient="records", date_format="iso")
        except KeyError as e:
            return {
                "error": f"请输入正确的参数错误 {e}，请升级 AKShare 到最新版本并在文档中确认该接口的使用方式：https://www.akshare.xyz"
            }, 404
        return json.loads(temp_df)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = '8080'
    from waitress import serve
    print("服务地址 http://{}:{}/".format(host, port))
    serve(app, host=host, port=port)
