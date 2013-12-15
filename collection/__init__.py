from bson.objectid import ObjectId

from collection.mongo import db
from collection.meta import generate_meta_information


class Image(object):
    @classmethod
    def create_from_dict(cls, data):
        if '_id' in data:
            data['id'] = data['_id']
            del data['_id']

        return cls(**data)

    def __init__(self, id=None, title=None,
                 description_url=None, image_url=None, source='wiki',
                 hash_value=None, hash_comparable_value=None):
        self.id = str(id)
        self.title = title
        self.description_url = description_url
        self.image_url = image_url
        self.source = source
        self.hash_value = hash_value
        self.hash_comparable_value = hash_comparable_value

    def __str__(self):
        return str(self.as_dict())
    
    def as_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'description_url': self.description_url,
            'image_url': self.image_url,
        }

    def full_as_dict(self):
        result = self.as_dict()
        result['hash_value'] = self.hash_value
        result['hash_comparable_value'] = self.hash_comparable_value

        return result


class ImageCollection(object):
    def __init__(self):
        self._collection = db.images

    def find(self, *args, **kwargs):
        return map(Image.create_from_dict, self._collection.find(*args, **kwargs))

    def remove(self, *args, **kwargs):
        return self._collection.remove(*args, **kwargs)

    def insert(self, obj):
        generate_meta_information(obj)

        dict_obj = obj.full_as_dict()

        if 'id' in dict_obj:
            del dict_obj['id']

        obj.id = str(self._collection.insert(dict_obj))
        return self

    def find_by_id(self, id):
        result = Image.create_from_dict(self._collection.find_one(ObjectId(id)))

        if result is None:
            raise Exception("there's no image with such id " + str(id))

        return result

    def find_by_hash_range(self, center, dispersion):
        return self.find({
            'hash_comparable_value': {
                '$gte': center - dispersion,
                '$lte': center + dispersion
            }
        })

    def save(self, image):
        if image.id is None:
            return self.insert(image)

        generate_meta_information(image)

        dict_obj = image.full_as_dict()
        dict_obj['id'] = ObjectId(image.id)

        self._collection.save(dict_obj)

image_collection = ImageCollection()
