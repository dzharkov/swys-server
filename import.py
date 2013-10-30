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
    from kooaba import upload_image
    from pymongo.helpers import shuffled

    logger = logging.getLogger(__name__)
    logger.info("Kooaba uploading " + str(count) + " images")

    images = shuffled(image_collection.find())

    for i in range(count):
        image = images[i]
        logger.info("Start uploading " + str(image))
        upload_image(image)


def kooaba_test(file):
    from collection import image_collection
    import urllib.request
    from kooaba import recognize_image

    logger = logging.getLogger(__name__)

    logger.info("Kooaba test: " + str(file))

    for img in recognize_image(file):
        print(str(img))

if __name__ == '__main__':

    handlers = {
        'wiki': wiki_import,
        'kooaba_upload': kooaba_upload,
        'kooaba_test': kooaba_test
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
