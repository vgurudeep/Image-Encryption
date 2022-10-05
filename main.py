import collections
import numpy as np
from PIL import Image
import time


def circular_left_shift(value, n):
    num_bits_in_int = 8
    n = n % num_bits_in_int
    mask = (1 << num_bits_in_int) - 1
    result = (value << n) | (value >> (num_bits_in_int - n))
    result = result & mask
    return result


def circular_right_shift(value, n):
    num_bits_in_int = 8
    n = n % num_bits_in_int
    mask = (1 << num_bits_in_int) - 1
    result = (value >> n) | (value << (num_bits_in_int - n))
    result = result & mask
    return result


def reversing_bits(num):
    bit_size = 8
    binary = bin(num)
    reverse = binary[-1:1:-1]
    reverse = reverse + (bit_size - len(reverse)) * '0'
    return int(reverse, 2)


start = time.time()
no_of_bits = 4
key = 13
encrypted_array = []
decrypted_array = []
reconstructed_array = []
reconstructed_array = np.zeros((183, 275, 3))
im = Image.open("big.jpg")

h, w = im.size

pixel_array = np.asarray(im)
shape = pixel_array.shape
print(shape)
flattend = pixel_array.flatten()

# Encryption
for rgb in flattend:
    level1_encryption = reversing_bits(rgb)  # Level 1 encryption
    level2_encryption = circular_left_shift(level1_encryption, no_of_bits)  # Level 2 encryption
    level3_encryption = level2_encryption ^ key  # Level 3 encryption

    encrypted_array.append(level3_encryption)

print(len(encrypted_array))

for rgb in encrypted_array:
    level1_decryption = rgb ^ key  # Level 1 decryption
    level2_decryption = circular_left_shift(level1_decryption, no_of_bits)  # Level 2 decryption
    level3_decryption = reversing_bits(level2_decryption)  # Level 3 decryption

    decrypted_array.append(level3_decryption)

reconstructed_array = np.reshape(decrypted_array, (w, h, 3))

print(np.array_equal(reconstructed_array, pixel_array))

img = Image.fromarray(reconstructed_array.astype(np.uint8))
img.save('reconstructed.jpg')
end = time.time()

print(end - start)
