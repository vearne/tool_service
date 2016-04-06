#encoding=utf-8
#!/usr/bin/python
from base62 import mid2str, str2mid
from time_tool import datetime2secs, secs2datetime
from tornado.escape import json_encode, json_decode
import tornado.ioloop
import tornado.web
import sys
import json
from datetime import datetime

class Base62Handler(tornado.web.RequestHandler):
    def post(self):
        params = json_decode(self.request.body)
        if params.get('mid'):
            mid = params.get('mid')
            ss = mid2str(mid)
            print 'ss', ss
            dd = {'ss':ss}
            self.write(dd)
        else:
            ss = params.get('ss')
            mid = str2mid(ss)
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

application = tornado.web.Application([
    (r"/base62", Base62Handler),
    (r"/timestamp", TimeStampHandler),
])

if __name__ == "__main__":
    print 'starting....'
    port = 9099
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
