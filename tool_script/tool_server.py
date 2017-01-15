#encoding=utf-8
#!/usr/bin/python
from mid_url import url_to_mid, mid_to_url 
from pingyin_tool import get_pingyin
from time_tool import datetime2secs, secs2datetime
from tornado.escape import json_encode, json_decode
import tornado.ioloop
import tornado.web
import sys
import json
from datetime import datetime

class MidURLHandler(tornado.web.RequestHandler):
    def post(self):
        params = json_decode(self.request.body)
        if params.get('mid'):
            mid = params.get('mid')
            ss = mid_to_url(mid)
            print 'ss', ss
            dd = {'ss':ss}
            self.write(dd)
        else:
            ss = params.get('ss')
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
            print ss
            d = secs2datetime(ss)
            dd = {'date': d.strftime('%Y-%m-%d %H:%M:%S')}
            self.write(dd)

class PingyinHandler(tornado.web.RequestHandler):
    def post(self):
        params = json_decode(self.request.body)
        content = params.get("content")
        dd = {'pingyin': get_pingyin(content)}
        self.write(dd)

application = tornado.web.Application([
    (r"/mid_url", MidURLHandler),
    (r"/pingyin", PingyinHandler),
    (r"/timestamp", TimeStampHandler),
])

if __name__ == "__main__":
    print 'starting....'
    port = 9099
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
