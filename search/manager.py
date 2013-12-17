from operator import itemgetter
from collection import image_collection
from image_hash import image_hash_manager, ImageHash
import itertools

import conf


class ImageSearchManager(object):
    def search(self, filename):
        given_image_hash = image_hash_manager.get_image_hash(filename)

        matched_images = []

        for image in image_collection.find_by_hash_range(given_image_hash.comparable_value(), conf.HASH_RANGE_VALUE):
            distance = ImageHash.build_from_str(image.hash_value).distance(given_image_hash)

            if distance < conf.HASH_DISTANCE_THRESHOLD:
                matched_images.append((image, distance))

        return itertools.islice(
            map(itemgetter(0), sorted(matched_images, key=itemgetter(1))),
            conf.FOUND_IMAGES_LIMIT
        )

image_search_manager = ImageSearchManager()
