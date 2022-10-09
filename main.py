import collections
import random
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


def rng():
    return random.randint(2 ** (6 - 1), 2 ** 6)


def prime_number_generator(product_of_ab):
    prime_list = []

    for i in range(product_of_ab + 1):
        prime_list.append(i)

    prime_list[0] = 0
    prime_list[1] = 0

    p = 2
    while p * p <= product_of_ab:
        # If prime[p] is not changed, then it is a prime
        if p != 0:
            # Update all multiples of p to zero
            for i in range(p * 2, product_of_ab + 1, p):
                prime_list[i] = 0

        p += 1

    updated_primes = list(filter(lambda x: x != 0, prime_list))
    # print("Possible prime numbers less than " + str(product_of_ab) + ": ")
    # print(*updated_primes)
    return random.choice(updated_primes)


random_number_a = rng()
random_number_b = rng()
while random_number_b == random_number_a:
    random_number_b == rng()

product = random_number_a * random_number_b
random_prime = prime_number_generator(product)

m = product - random_prime
e = m + random_number_a
d = m + random_number_b
n = int(((e * d) - random_prime) / m)
q = pow(random_prime, -1, mod=n)


start = time.time()

encrypted_array = []
decrypted_array = []
reconstructed_array = []
# reconstructed_array = np.zeros((183, 275, 3))
im_name = input("Enter the image (with file extension): ")
no_of_bits = int(input("Enter the number of bits to be shifted: "))
key = int(input("Enter the key value: "))
im = Image.open(im_name)

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
    level4_encryption = int(pow((level3_encryption * q), 1, n)) # Level 4 encryption
    encrypted_array.append(level4_encryption)

print(len(encrypted_array))

for rgb in encrypted_array:
    level1_decryption = (rgb * e * d) % n
    level2_decryption = level1_decryption ^ key  # Level 1 decryption
    level3_decryption = circular_right_shift(level2_decryption, no_of_bits)  # Level 2 decryption
    level4_decryption = reversing_bits(level3_decryption)  # Level 3 decryption

    decrypted_array.append(level4_decryption)

reconstructed_array = np.reshape(decrypted_array, (w, h, 3))

print(np.array_equal(reconstructed_array, pixel_array))

img = Image.fromarray(reconstructed_array.astype(np.uint8))
img.save('reconstructed.jpg')
end = time.time()

print(end - start)
