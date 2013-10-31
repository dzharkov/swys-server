from urllib.parse import urlparse
from http import client as httplib
import email.utils
import mimetypes
import json
import logging

from .ka_signature import KASignature

version = '1.2.0'

# Configuration

# with KA auth, both http and https are possible
UPLOAD_ENDPOINT = 'https://upload-api.kooaba.com/'
QUERY_ENDPOINT = 'https://query-api.kooaba.com/v4/query'

logger = logging.getLogger(__name__)


class BasicAPIClient:
    """ Client for kooaba  API V4. """

    def __init__(self, secret_token, key_id=None):
        self.KA = KASignature(secret_token)
        self.key_id = key_id
        self.secret_token = secret_token


    def _query_request_args(self, data, auth_method='Token'):
        content_type, body = self.encode_multipart_formdata([], [('image', data)])

        return 'POST', QUERY_ENDPOINT, bytearray(body), content_type, auth_method

    def query(self, filename, auth_method='Token'):
        data, content_type = self.data_from_file(filename)
        return self._send_request(*self._query_request_args(data, auth_method))

    def _create_item_request_args(self, bucket_id, title, refid, json_string):
        url = UPLOAD_ENDPOINT+'api/v4/buckets/'+bucket_id+'/items'

        metadata = json.loads(json_string)
        data = {"title":title, "reference_id":refid, "metadata":metadata}

        return 'POST', url, json.dumps(data), 'application/json'

    def create_item(self, bucket_id, title, refid, json_string):
        return self._send_request(*self._create_item_request_args(bucket_id, title, refid, json_string))

    def _attach_image_request_args(self, bucket_id, item_id, content_type, data):
        url = UPLOAD_ENDPOINT+'api/v4/items/'+item_id+'/images'

        return 'POST', url, bytearray(data), content_type

    def attach_image(self, bucket_id, item_id, content_type, data):
        return self._send_request(*self._attach_image_request_args(bucket_id, item_id, content_type, data))

    def _replace_metadata_request_args(self, item_id, json_string):
        url = UPLOAD_ENDPOINT+'api/v4/items/'+item_id
        metadata = json.loads(json_string)
        data = {"metadata": metadata}

        return 'PUT', url, json.dumps(data), 'application/json'

    def replace_metadata(self, item_id, json_string):
        return self._send_request(*self._replace_metadata_request_args(item_id, json_string))

    def data_from_file(self,filename):
        content_type, _encoding = mimetypes.guess_type(filename)
        with open(filename, 'rb') as f:
            return f.read() , content_type

    def _prepare_headers(self, method, api_path, data=None, content_type=None, auth_method='Token'):
        parsed_url = urlparse(api_path)

        date = email.utils.formatdate(None, localtime=False, usegmt=True)

        if auth_method=='KA':
            signature = self.KA.sign(method, data, content_type, date, parsed_url.path)
            headers = {'Authorization': 'KA %s:%s' % (self.key_id,signature.decode('utf-8')), 'Date': date}
            logger.info("signature: %s", headers['Authorization'])
        else: # Token
            headers = {'Authorization': 'Token %s' % self.secret_token,'Date': date}

        if content_type is not None:
            headers['Content-Type'] = content_type

        if data is not None:
            headers['Content-Length'] = str(len(data))

        return headers

    def _send_request(self, method, api_path, data=None, content_type=None, auth_method='Token'):
        if data is None:
            logger.info("> %s %s", method, api_path)
        elif len(data) < 4096:
            logger.info("> %s %s: > %s", method, api_path, data)
        else:
            logger.info("> %s %s: %sB", method, api_path, len(data))

        return self._send_http_request(method, api_path, data, self._prepare_headers(method, api_path, data, content_type, auth_method))

    def _process_http_response(self, body):
        return json.loads(body.decode('utf-8'))

    def _send_http_request(self, method, url, data, headers):
        parsed_url = urlparse(url)

        port = parsed_url.port
        if port is None:
            port = 80
            if (parsed_url.scheme == 'https'):
               port = 443

        host = parsed_url.hostname

        if (parsed_url.scheme == 'https'):
            http = httplib.HTTPSConnection(host, port )
        elif (parsed_url.scheme == 'http'):
            http = httplib.HTTPConnection(host, port )
        else:
            raise RuntimeError("URL scheme '%s' not supported" % parsed_url.scheme)

        try:
            http.request(method, parsed_url.path, body=data,  headers=headers)
            response = http.getresponse()
            # we have to read the response before the http connection is closed
            body = response.read()
            logger.info("< %d %s", response.status, response.reason)
            logger.info("< %s", body)

            return self._process_http_response(body)
        finally:
            http.close()


    def encode_multipart_formdata(self, fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """

        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = b'\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s";' % key)
            L.append('Content-Type: %s' % 'application/octet-stream')
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(map(lambda x: x.encode('utf-8') if not isinstance(x, bytes) else x, L))
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body