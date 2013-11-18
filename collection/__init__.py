from collection.mongo import db
from bson.objectid import ObjectId


class Image(object):
    @classmethod
    def create_from_dict(cls, data):
        if '_id' in data:
            data['id'] = data['_id']
            del data['_id']

        return cls(**data)

    def __init__(self, id=None, title=None, description_url=None, image_url=None, source='wiki'):
        self.id = str(id)
        self.title = title
        self.description_url = description_url
        self.image_url = image_url
        self.source = source

    def __str__(self):
        return str(self.as_dict())
    
    def as_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'description_url': self.description_url,
            'image_url': self.image_url,
        }


class ImageCollection(object):
    def __init__(self):
        self._collection = db.images

    def find(self, *args, **kwargs):
        return map(Image.create_from_dict, self._collection.find(*args, **kwargs))

    def remove(self, *args, **kwargs):
        return self._collection.remove(*args, **kwargs)

    def insert(self, obj):
        dict_obj = obj.as_dict()

        if 'id' in dict_obj:
            del dict_obj['id']

        obj.id = str(self._collection.insert(dict_obj))
        return self

    def find_by_id(self, id):
        result = Image.create_from_dict(self._collection.find_one(ObjectId(id)))

        if result is None:
            raise Exception("there's no image with such id " + str(id))

        return result

image_collection = ImageCollection()
