import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def on_complete(self, result, exc=None):
        if exc is not None:
            self.write_error(200, exc_info=(exc.__class__, exc, None))
            return

        if isinstance(result, bool):
            result = {
                'result': 1 if result else 0
            }
        elif isinstance(result, map) or isinstance(result, list) or isinstance(result, filter):
            result = {
                'data': list(
                    map(lambda o: o.as_dict() if hasattr(o, 'as_dict') else o, result)
                )
            }
        elif hasattr(result, 'as_dict'):
            result = result.as_dict()

        if not isinstance(result, dict):
            result = {'data' : result}

        if 'result' not in result:
            result['result'] = 1


        self.write(result)
        self.finish()

    def handle_request(self, *args, **kwargs):
        raise NotImplemented

    def handle_request_async(self, *args, **kwargs):
        try:
            result = self.handle_request(*args, **kwargs)
        except Exception as exc:
            self.on_complete(None, exc=exc)
        else:
            self.on_complete(result)

    def post(self, *args, **kwargs):
        return self.handle_request_async(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.handle_request_async(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.handle_request_async(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.handle_request_async(*args, **kwargs)


class CollectionBaseHandler(BaseHandler):
    @classmethod
    def create_mappings(cls, prefix):
        return [
            ('/{0}/?'.format(prefix), cls),
            ('/{0}/(?P<id>[^/]+)/?'.format(prefix), cls)
        ]

    collection = None

    def handle_request(self, id=None):
        if id is None:
            offset = self.get_argument('offset', 0)
            limit = self.get_argument('limit', 10)
            return self.collection.find(skip=int(offset), limit=int(limit))

        return self.collection.find_by_id(id)
