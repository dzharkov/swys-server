import logging
import tornado.gen

from .bridge import SwysKooabaBridge
from .async_api import AsyncApiClient

logger = logging.getLogger(__name__)

class AsyncSwysKooabaBridge(SwysKooabaBridge):
    api_cls = AsyncApiClient

    @tornado.gen.coroutine
    def recognize_image(self, filename, data=None):
        try:
            result = yield self.query_api_client.query(filename, data=data, auth_method='KA')
        except:
            logger.info("Async recognition query has failed")
            raise

        return self._process_recognition_result(result)

kooaba_bridge = AsyncSwysKooabaBridge()
