#!/usr/bin/env python3

from collection.wiki_import import import_images

if __name__ == '__main__':
    res = input("Do you really want to import images from wiki?[Y/n]").lower()
    if res == 'y':
        import_images()
    else:
        print("Aborted")