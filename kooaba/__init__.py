import urllib.request
import conf
import logging
from .api import BasicAPIClient

logger = logging.getLogger(__name__)

data_api_client = BasicAPIClient(conf.KOOABA_DATA_KEY_SECRET_TOKEN)


def upload_image(image):
    tmp_file = urllib.request.urlretrieve(image.image_url)[0]

    logger.info("Uploading " + str(tmp_file))
    data, content_type = data_api_client.data_from_file(tmp_file)

    try:
        item = data_api_client.create_item(conf.KOOABA_BUCKET_ID, image.title, image.id, '{}')
        logger.info('created item %s', item['uuid'])
        images = data_api_client.attach_image(conf.KOOABA_BUCKET_ID, item['uuid'], content_type, data)
        logger.info('attached image %s', images[0]['sha1'])
    except:
        logger.exception('Upload failed')
        raise
