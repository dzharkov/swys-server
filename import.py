#!/usr/bin/env python3
import argparse
import sys
import logging


from collection.wiki_import import import_images
from collection import Image, image_collection

def wiki_import():
    res = input("Do you really want to import images from wiki?[Y/n]").lower()
    if res == 'y':
        import_images()
    else:
        print("Aborted")

def kooaba_upload(count):
    from kooaba.bridge import kooaba_bridge
    from pymongo.helpers import shuffled

    logger = logging.getLogger(__name__)
    logger.info("Kooaba uploading " + str(count) + " images")

    images = shuffled(image_collection.find())

    for i in range(count):
        image = images[i]
        logger.info("Start uploading " + str(image))
        kooaba_bridge.upload_image(image)


def kooaba_test(file):
    from kooaba.bridge import kooaba_bridge

    logger = logging.getLogger(__name__)

    logger.info("Kooaba test: " + str(file))

    for img in kooaba_bridge.recognize_image(file):
        print(str(img))


def add_image():

    image = Image.create_from_dict({
        'title': input("Title: "),
        'image_url': input("Image URL: "),
        'description_url': input("Description URL: "),
        'source': 'manual',
    })

    image_collection.save(image)

    need_import = input("Import image to kooaba?[Y/n]").lower() == 'y'

    if need_import:
        from kooaba.bridge import kooaba_bridge
        kooaba_bridge.upload_image(image)


def update_meta():
    for image in image_collection.find():
        image_collection.save(image)

def create_thumbnails():
    from collection.meta import create_thumbnail
    import threading
    import queue

    logger = logging.getLogger(__name__)

    images_queue = queue.Queue()

    def consume():
        while True:
            image = images_queue.get()
            create_thumbnail(image)
            logger.info('thread: '+ str(threading.current_thread().ident))
            logger.info("Creating thumbnail for: " + image.title)
            images_queue.task_done()

    for i in range(10):
        threading.Thread(target=consume, daemon=True).start()

    for image in image_collection.find():
        images_queue.put(image)

    images_queue.join()

if __name__ == '__main__':

    handlers = {
        'wiki': wiki_import,
        'add_image': add_image,
        'kooaba_upload': kooaba_upload,
        'kooaba_test': kooaba_test,
        'update_meta': update_meta,
        'create_thumbnails': create_thumbnails,
    }

    log_levels_map = {'info': logging.INFO, 'error': logging.ERROR}

    parser = argparse.ArgumentParser()

    parser.add_argument('--log_level', choices=log_levels_map.keys(), default='error')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('wiki')

    kooaba_parser = subparsers.add_parser('kooaba_upload')
    kooaba_parser.add_argument('--count', type=int, default=10)

    kooaba_test_parser = subparsers.add_parser('kooaba_test')
    kooaba_test_parser.add_argument('file')

    subparsers.add_parser('add_image')
    subparsers.add_parser('update_meta')
    subparsers.add_parser('create_thumbnails')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    command = args.command
    logging.basicConfig(level=log_levels_map[args.log_level])

    cmd_args = vars(args)

    del cmd_args['command']
    del cmd_args['log_level']

    handlers[command](**cmd_args)
