#encoding=utf-8
#!/usr/bin/python
from mid_url import url_to_mid, mid_to_url 
from pingyin_tool import get_pingyin
from time_tool import datetime2secs, secs2datetime
from ip_tool  import int2ip, ip2int 
from domain_tool  import evaluate 
from tornado.escape import json_encode, json_decode
import tornado.ioloop
import tornado.web
import sys
import json
from datetime import datetime

class MidURLHandler(tornado.web.RequestHandler):
    def options(self):
        self.set_header("Allow","POST, OPTIONS");

    def post(self):
        params = json_decode(self.request.body)
        if params.get('mid'):
            mid = params.get('mid')
            print "mid", mid
            ss = mid_to_url(mid)
            dd = {'url':ss}
            self.write(dd)
        else:
            ss = params.get('url')
            mid = url_to_mid(ss)
            print 'mid', mid
            dd = {'mid':mid}
            self.write(dd)

class TimeStampHandler(tornado.web.RequestHandler):
    def post(self):
        params = json_decode(self.request.body)
        if params.get('date'):
            d = params.get('date')
            print d
            d = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
            print d
            sec = datetime2secs(d)
            dd = {'sec':sec}
            self.write(dd)
        else:
            ss = params.get('sec')
            ss = float(ss)
            d = secs2datetime(ss)
            dd = {'date': d.strftime('%Y-%m-%d %H:%M:%S')}
            self.write(dd)

class PingyinHandler(tornado.web.RequestHandler):
    def post(self):
        params = json_decode(self.request.body)
        content = params.get("content")
        dd = {'pinyin': get_pingyin(content)}
        self.write(dd)

class IPHandler(tornado.web.RequestHandler):
    def post(self):
        params = json_decode(self.request.body)
        ip = params.get("ip")
        if ip:
            dd = {'integer': ip2int(ip)}
            self.write(dd)
        else:
            integer = params.get("integer")
            print integer
            dd = {'ip': int2ip(integer)}
            self.write(dd)

class DomainHandler(tornado.web.RequestHandler):
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
    print 'starting....'
    port = 9099
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
