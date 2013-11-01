import tornado.gen

from webapi import BaseHandler
from kooaba.async_bridge import kooaba_bridge

from collection import image_collection


class SearchRequestHandler(BaseHandler):
    @tornado.gen.coroutine
    def handle_request(self, *args, **kwargs):
        files = self.request.files.get('image', [])

        if len(files) == 0:
            raise Exception("there is no file attached")

        file = files[0]

        return (yield kooaba_bridge.recognize_image(file.filename, file.body))

import random


class RandomSearchRequestHandler(BaseHandler):
    def initialize(self):
        super().initialize()
        from pymongo.helpers import shuffled

        self.shuffled_collection = shuffled(image_collection.find())
        self.counter = 0

    def handle_request(self, *args, **kwargs):
        amount = min(
            random.randint(1, 4),
            len(self.shuffled_collection) - self.counter
        )

        result = self.shuffled_collection[self.counter:amount]

        self.counter = (self.counter + amount) % len(self.shuffled_collection)

        return result
