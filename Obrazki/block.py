from PIL import Image
import hashlib
import random

block_size = 8

# Read input image
input_image = Image.open("plain.bmp")
size = input_image.size
image_data = input_image.tobytes()

# Read key from file
try:
    with open("key.txt", "rb") as f:
        key = f.read()
    if len(key) != block_size:
        raise ValueError(f"Key size must be {block_size} bytes")
except FileNotFoundError:
    keys = []
    for x in range(block_size):
        key = hashlib.md5(str(random.random() * x).encode("UTF-8")).digest()
        keys.append(key)
# ECB
new_data = []
for x in range(size[0]):
    for y in range(size[1]):
        pp = x * size[0] + y  # pixel position
        op = image_data[pp]  # original pixel
        pta = op ^ key[y % block_size]  # pixel to add
        new_data.append(pta)

output_image = input_image.copy()
output_image.frombytes(bytes(new_data))
output_image.save("ecb_crypto.bmp")
print("ECB Done")

# CBC
new_key = 13
new_data = [image_data[0] ^ new_key]
for x in range(size[0] * size[1]):
    new_data.append(new_data[x - 1] ^ image_data[x] ^ key[x % block_size])

output_image = input_image.copy()
output_image.frombytes(bytes(new_data))
output_image.save("cbc_crypto.bmp")
print("CBC Done")
