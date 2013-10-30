import urllib.request
import conf
import logging
from .api import BasicAPIClient
from collection import image_collection

logger = logging.getLogger(__name__)

data_api_client = BasicAPIClient(conf.KOOABA_DATA_KEY_SECRET_TOKEN)
query_api_client = BasicAPIClient(conf.KOOABA_QUERY_SECRET_TOKEN, conf.KOOABA_QUERY_KEY_ID)


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


def recognize_image(file):
    logger.info("Recognition of " + file)

    try:
        result = query_api_client.query(file, 'KA')
    except:
        logger.info("Recognition query has failed")
        raise

    return map(lambda x: image_collection.find_by_id(x['reference_id']), result['results'])
