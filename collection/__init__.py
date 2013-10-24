
class Image(object):
    def __init__(self, id=None, title=None, description_url=None, image_url=None):
        self.id = id
        self.title = title
        self.description_url = description_url
        self.image_url = image_url

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description_url': self.description_url,
            'image_url': self.image_url,
        }


class ImageCollection(object):
    def __init__(self):
        self._collection = [
            Image(
                id='1',
                title='Хутор в Малороссии (1884)',
                description_url='http://ru.wikipedia.org/wiki/%D0%9A%D1%80%D1%8B%D0%B6%D0%B8%D1%86%D0%BA%D0%B8%D0%B9,_%D0%9A%D0%BE%D0%BD%D1%81%D1%82%D0%B0%D0%BD%D1%82%D0%B8%D0%BD_%D0%AF%D0%BA%D0%BE%D0%B2%D0%BB%D0%B5%D0%B2%D0%B8%D1%87',
                image_url='http://upload.wikimedia.org/wikipedia/commons/thumb/5/51/KonstantinKryzhitsky_HutorVMalorossii_1884.jpg/640px-KonstantinKryzhitsky_HutorVMalorossii_1884.jpg?uselang=ru',
            ),
            Image(
                id='2',
                title='Данте Габриэль Россетти',
                description_url='http://allday2.com/engine/print.php?newsid=81490',
                image_url='http://i.allday.ru/uploads/posts/2009-01/1232719137_3.jpg'
            )
        ]

    def _find_by_id(self, id):
        return filter(lambda x: x.id == str(id), self._collection)

    def find_by_id(self, id):
        result = list(self._find_by_id(id))

        if len(result) != 1:
            raise Exception("more than one image was found with id " + str(id))
        if len(result) == 0:
            raise Exception("there's no image with such id " + str(id))

        return result[0]

image_collection = ImageCollection()
