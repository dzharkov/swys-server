import urllib.request

from image_hash import image_hash_manager

def download_image(image):
    return urllib.request.urlretrieve(image.image_url)[0]

def generate_meta_information(image):
    tmp_file = download_image(image)

    image_hash = image_hash_manager.get_image_hash(tmp_file)

    image.hash_value = str(image_hash)
    image.hash_comparable_value = image_hash.comparable_value()

def create_thumbnail(image):
    import conf
    import os
    from PIL import Image

    if not os.path.exists(conf.STATIC_ROOT):
        os.mkdir(conf.STATIC_ROOT)

    if not os.path.exists(conf.THUMBNAIL_ROOT):
        os.mkdir(conf.THUMBNAIL_ROOT)

    if image.thumbnail_exists:
        return

    tmp_file = download_image(image)
    pil_img = Image.open(tmp_file)

    height = conf.THUMBNAIL_HEIGHT
    height_fraction = height / float(pil_img.size[1])
    width = int(float(pil_img.size[0]) * float(height_fraction))

    resized = pil_img.resize((width, height), Image.ANTIALIAS)

    resized.save(image.thumbnail_path)
