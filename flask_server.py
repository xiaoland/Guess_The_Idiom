# coding=utf-8
# author: Lan_zhijiang
# description: http server (build by flask)
# date: 2020/12/12

from flask import Flask, request
from BotServer import application
import json
import socket

flask_app = Flask(__name__)
log_class = {}
settings = {}


def get_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def run_server():

    """
    启动服务器
    :return:
    """
    print("HttpServer: Start http server...", 1)

    ip = get_ip()
    print("HttpServer: ServerAddr: " + ip + ":6001", 1)
    flask_app.run(host=ip, port=6001)


@flask_app.route('/', methods=["POST", "GET", "HEAD"])
def route_api():

    """
    处理请求到/api路径下的请求
    :return:
    """
    return json.dumps(application(request.method, request.get_data()))


if __name__ == "__main__":
    run_server()
