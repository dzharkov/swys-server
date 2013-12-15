#!/usr/bin/env python3
import argparse
import sys
import logging


from collection.wiki_import import import_images

def wiki_import():
    res = input("Do you really want to import images from wiki?[Y/n]").lower()
    if res == 'y':
        import_images()
    else:
        print("Aborted")

def kooaba_upload(count):
    from collection import image_collection
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
    from collection import Image, image_collection

    image = Image.create_from_dict({
        'title': input("Title: "),
        'image_url': input("Image URL: "),
        'description_url': input("Description URL: "),
        'source': 'manual',
    })

    image_collection.insert(image)

    need_import = input("Import image to kooaba?[Y/n]").lower() == 'y'

    if need_import:
        from kooaba.bridge import kooaba_bridge
        kooaba_bridge.upload_image(image)


def update_meta():
    from collection import image_collection

    for image in image_collection.find():
        image_collection.save(image)


if __name__ == '__main__':

    handlers = {
        'wiki': wiki_import,
        'add_image': add_image,
        'kooaba_upload': kooaba_upload,
        'kooaba_test': kooaba_test,
        'update_meta': update_meta,
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

    add_image_parser = subparsers.add_parser('add_image')
    update_meta_parser = subparsers.add_parser('update_meta')

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
