#!/usr/bin/env python3

import tornado.web
import tornado.ioloop

from collection.request_handler import ImageCollectionRequestHandler


import conf

application = tornado.web.Application(
    ImageCollectionRequestHandler.create_mappings('image') + [],
    debug=conf.DEBUG
)

application.listen(conf.PORT)
tornado.ioloop.IOLoop.instance().start()
