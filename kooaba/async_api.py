import logging
from tornado import httpclient
from tornado import gen
from .api import BasicAPIClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class AsyncApiClient(BasicAPIClient):

    def __init__(self, secret_token, key_id=None):
        super().__init__(secret_token, key_id)
        self.http_client = httpclient.AsyncHTTPClient()

    @gen.coroutine
    def query(self, filename, data=None, auth_method='Token'):
        if data is None:
            data = self.data_from_file(filename)

        return (yield self._send_request(*self._query_request_args(data, auth_method)))

    def attach_image(self, bucket_id, item_id, content_type, data):
        raise NotImplemented()

    def create_item(self, bucket_id, title, refid, json_string):
        raise NotImplemented()

    def replace_metadata(self, item_id, json_string):
        raise NotImplemented()

    @gen.coroutine
    def _send_request(self, method, api_path, data=None, content_type=None, auth_method='Token'):
        headers = self._prepare_headers(method, api_path, data, content_type, auth_method)

        return (yield self._send_http_request(method, api_path, data, headers))

    @gen.coroutine
    def _send_http_request(self, method, url, data, headers):
        response = yield self.http_client.fetch(
            httpclient.HTTPRequest(url=url, method=method, body=bytes(data), headers=headers),
        )

        return self._process_http_response(response.body)
