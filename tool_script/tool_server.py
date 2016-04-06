#encoding=utf-8
#!/usr/bin/python
from base62 import mid2str, str2mid
from tornado.escape import json_encode, json_decode
import tornado.ioloop
import tornado.web
import sys
import json

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

application = tornado.web.Application([
    (r"/base62", Base62Handler),
])

if __name__ == "__main__":
    print 'starting....'
    port = 9099
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
