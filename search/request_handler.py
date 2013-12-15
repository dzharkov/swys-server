import json
import tempfile
import tornado.gen
import tornado.web
import zmq

from webapi import BaseHandler
from kooaba.async_bridge import kooaba_bridge

from collection import image_collection
from zmq.eventloop.zmqstream import ZMQStream

import conf


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

context = zmq.Context()


class SwysSearchRequestHandler(BaseHandler):
    def initialize(self):
        socket = context.socket(zmq.REQ)
        socket.connect(conf.SEARCH_WORKER_ZMQ_ENDPOINT)

        self._zmq_stream = ZMQStream(socket)
        self._zmq_stream.on_recv(self._recv_result, copy=True)

    @tornado.web.asynchronous
    def handle_request_async(self, *args, **kwargs):

        files = self.request.files.get('image', [])

        if len(files) == 0:
            raise Exception("there is no file attached")

        file = files[0]

        temp_file = tempfile.NamedTemporaryFile('wb', delete=False)
        temp_file.write(file.body)

        self._zmq_stream.send_json({'filename': temp_file.name})

    def _recv_result(self, msg):

        result_str = "".join(( part.decode('utf-8') for part in msg ))
        result = json.loads(result_str)['data']

        return self.on_complete(result)

