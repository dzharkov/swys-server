import re
from urllib.parse import unquote
from urllib.error import URLError

from collection import image_collection, Image
from wikipedia import wikipedia

def import_images_from_page(title):
    print("Importing from [" + title + "]")
    try:
        p = wikipedia.page(title)
    except wikipedia.PageError as e:
        print("could not load the page: " + str(e))
        return

    query_params = {
        'generator': 'images',
        'gimlimit': 'max',
        'prop': 'imageinfo',
        'iiprop': 'url',
        'titles': p.title,
    }
    try:
        request = wikipedia._wiki_request(**query_params)

        image_keys = request['query']['pages'].keys()
        images = (request['query']['pages'][key] for key in image_keys)
        urls_and_desc = filter(
            lambda x: re.search(r'(?:jpg|jpeg)$', x[0].lower()),
            ((image['imageinfo'][0]['url'], image['imageinfo'][0]['descriptionurl']) for image in images if image.get('imageinfo'))
        )
    except KeyError or URLError as e:
        print("could not load page images: " + str(e))
        return

    for item in urls_and_desc:
        match = re.search(r'File:(.*?)(?:[0-9]{3})?\.(?:jpg|jpeg)$', unquote(item[1]))

        if match is None:
            continue

        file_title = re.sub(r'[_-]+', ' ', match.group(1)).strip()

        image = Image.create_from_dict({
            'title': file_title,
            'image_url': item[0],
            'description_url': item[1],
            'source': 'wiki',
        })

        image_collection.insert(image)


def import_images():
    image_collection.remove(source='wiki')

    wikipedia.set_lang('ru')
    root_page = wikipedia.page('Экспонаты эрмитажа')

    for link in root_page.links:
        import_images_from_page(link)
