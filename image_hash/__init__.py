from PIL import Image
import numpy

from image_hash.algorithms import *

HASH_SIZE = 32
HASH_LENGTH = HASH_SIZE * HASH_SIZE // 4
HASH_LENGTH_BINARY = HASH_SIZE * HASH_SIZE


class ImageHash(object):
    @classmethod
    def _prepend_zeros(cls, value, length):
        if len(value) < length:
            value = ('0' * (length - len(value))) + value

        return value

    @classmethod
    def build_from_str(cls, str_hash):

        assert len(str_hash) == HASH_LENGTH

        int_value = int('0x' + str_hash, 16)
        bin_value = cls._prepend_zeros(bin(int_value)[2:], HASH_LENGTH_BINARY)

        return ImageHash(
            numpy.array(
                [v == '1' for v in bin_value],
                dtype=numpy.bool
            )
        )

    def __init__(self, binary_array):
        self._hash = binary_array.flatten()

    def distance(self, other):
        return ((self._hash != other._hash).sum()) / HASH_LENGTH_BINARY

    def comparable_value(self):
        return sum([1 for v in self._hash if v])

    def __str__(self):
        result = hex(
            int(
                "".join(
                    map(
                        lambda x: str(int(x)),
                        self._hash
                    )
                ),
            2)
        )[2:]

        return self._prepend_zeros(result, HASH_LENGTH)

class ImageHashManager(object):
    algorithms = {'diff_hash': diff_hash}

    def __init__(self, default_algorithm='diff_hash'):
        self._default_algorithm = default_algorithm

    def _choose_algorithm(self, algorithm_name):
        return self.algorithms[algorithm_name]

    def get_image_hash(self, filename):
        img = Image.open(filename)
        return ImageHash(
            self._choose_algorithm(self._default_algorithm)(img, HASH_SIZE)
        )

image_hash_manager = ImageHashManager()
