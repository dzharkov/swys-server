#!/usr/bin/env python3

import tornado.web
import tornado.ioloop


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish({'result': 1})

import conf

application = tornado.web.Application([
    (r"/", BaseHandler)
], debug=conf.DEBUG)

application.listen(conf.PORT)
tornado.ioloop.IOLoop.instance().start()
