#!/usr/bin/env python3

import logging
import tornado.web
import tornado.ioloop

from zmq.eventloop import ioloop
ioloop.install()

from collection.request_handler import ImageCollectionRequestHandler
from search.request_handler import SearchRequestHandler, RandomSearchRequestHandler, SwysSearchRequestHandler

import conf

if conf.DEBUG:
    logging.basicConfig(level=logging.DEBUG)

application = tornado.web.Application(
    ImageCollectionRequestHandler.create_mappings('image') + [
        ('/search/?', SearchRequestHandler),
        ('/search/random/?', RandomSearchRequestHandler),
        ('/search/swys/?', SwysSearchRequestHandler),
    ],
    debug=conf.DEBUG
)

application.listen(conf.PORT)
tornado.ioloop.IOLoop.instance().start()
