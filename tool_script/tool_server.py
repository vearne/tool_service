# encoding=utf-8
# !/usr/bin/python
from mid_url import url_to_mid, mid_to_url
from pingyin_tool import get_pingyin
from ip_tool import int2ip, ip2int
from domain_tool import evaluate
from tornado.escape import json_encode, json_decode
import tornado.ioloop
import tornado.web
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import arrow


class MidURLHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)  # 起线程池，由当前RequestHandler持有

    def options(self):
        self.set_header("Allow", "POST, OPTIONS");

    @tornado.gen.coroutine
    def post(self):
        params = json_decode(self.request.body)
        if params.get('mid'):
            mid = params.get('mid')
            print('mid', mid)
            ss = mid_to_url(mid)
            dd = {'url': ss}
            self.write(dd)
        else:
            ss = params.get('url')
            mid = url_to_mid(ss)
            print('mid', mid)
            dd = {'mid': mid}
            self.write(dd)


class TimeStampHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    @tornado.gen.coroutine
    def post(self):
        params = json_decode(self.request.body)
        if params.get('date'):
            d = params.get('date')
            print(d)
            d += "+08:00"
            sec = int(arrow.get(d).timestamp())
            dd = {'sec': sec}
            self.write(dd)
        else:
            ss = params.get('sec')
            ss = float(ss)
            t = arrow.get(ss)
            t = t.to("+08:00")
            dd = {'date': t.format('YYYY-MM-DD HH:mm:ss')}
            self.write(dd)


class PingyinHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    @tornado.gen.coroutine
    def post(self):
        params = json_decode(self.request.body)
        content = params.get("content")
        dd = {'pinyin': get_pingyin(content)}
        self.write(dd)


class IPHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    @tornado.gen.coroutine
    def post(self):
        params = json_decode(self.request.body)
        ip = params.get("ip")
        if ip:
            dd = {'integer': ip2int(ip)}
            self.write(dd)
        else:
            integer = params.get("integer")
            print(integer)
            dd = {'ip': int2ip(integer)}
            self.write(dd)


class DomainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    @tornado.gen.coroutine
    def post(self):
        params = json_decode(self.request.body)
        domain = params.get("domain")
        domain = domain.strip()
        self.write(evaluate(domain))


application = tornado.web.Application([
    (r"/api/mid_url", MidURLHandler),
    (r"/api/pinyin", PingyinHandler),
    (r"/api/timestamp", TimeStampHandler),
    (r"/api/ip", IPHandler),
    (r"/api/domain", DomainHandler),
])

if __name__ == "__main__":
    print('starting....')
    port = 9099
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    server = tornado.httpserver.HTTPServer(application)
    server.bind(port)
    server.start(2)  # forks one process per cpu
    tornado.ioloop.IOLoop.current().start()
