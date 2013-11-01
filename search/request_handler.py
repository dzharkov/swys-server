import tornado.gen
from webapi import BaseHandler
from kooaba.async_bridge import kooaba_bridge


class SearchRequestHandler(BaseHandler):
    @tornado.gen.coroutine
    def handle_request(self, *args, **kwargs):
        files = self.request.files.get('image', [])

        if len(files) == 0:
            raise Exception("there is no file attached")

        file = files[0]

        return (yield kooaba_bridge.recognize_image(file.filename, file.body))
