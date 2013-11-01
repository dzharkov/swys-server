#!/usr/bin/env python3

import tornado.web
import tornado.ioloop

from collection.request_handler import ImageCollectionRequestHandler
from search.request_handler import SearchRequestHandler, RandomSearchRequestHandler


import conf

application = tornado.web.Application(
    ImageCollectionRequestHandler.create_mappings('image') + [
        ('/search/?', SearchRequestHandler),
        ('/search/random/?', RandomSearchRequestHandler),
    ],
    debug=conf.DEBUG
)

application.listen(conf.PORT)
tornado.ioloop.IOLoop.instance().start()
