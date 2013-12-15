import urllib.request

from image_hash import image_hash_manager


def generate_meta_information(image):

    tmp_file = urllib.request.urlretrieve(image.image_url)[0]
    image_hash = image_hash_manager.get_image_hash(tmp_file)

    image.hash_value = str(image_hash)
    image.hash_comparable_value = image_hash.comparable_value()

