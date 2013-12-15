from PIL import Image
import numpy
import scipy.fftpack

def average_hash(image, hash_size=8):
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)

    pixels = numpy.array(image.getdata()).reshape((hash_size, hash_size))
    avg = pixels.mean()
    diff = pixels > avg

    return diff


def perceptual_hash(image, hash_size=32):
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)

    pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((hash_size, hash_size))
    dct = scipy.fftpack.dct(pixels)
    dctlowfreq = dct[:8, 1:9]

    avg = dctlowfreq.mean()
    diff = dctlowfreq > avg

    return diff

def diff_hash(image, hash_size=8):
    image = image.convert("L").resize((hash_size + 1, hash_size), Image.ANTIALIAS)

    pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((hash_size + 1, hash_size))

    diff = pixels[1:] > pixels[-1:]

    return diff
