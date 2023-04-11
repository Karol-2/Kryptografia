from PIL import Image
import hashlib
import random

input_image = Image.open("plainfb.bmp")

block_size = 8
image_data = input_image.tobytes()
size = input_image.size

# ECB
new_data = []
keys = []
for x in range(block_size):
    key = hashlib.md5(str(random.random() * x).encode("UTF-8")).digest()
    keys.append(key)

for x in range(size[0]):
    for y in range(size[1]):
        pp = x * size[0] + y  # pixel position
        op = image_data[pp]  # original pixel
        pta = op ^ keys[x % block_size][y % block_size]     # pixel to add
        new_data.append(pta)

output_image = input_image.copy()
output_image.frombytes(bytes(new_data))
output_image.save("ecb_crypto.bmp")
print("ECB Done")

# CBC
new_key = 13
new_data = [image_data[0] ^ new_key]
for x in range(size[0]*size[1]):
    new_data.append(new_data[x-1] ^ image_data[x] ^ keys[x%64//8][x%8])

output_image = input_image.copy()
output_image.frombytes(bytes(new_data))
output_image.save("cbc_crypto.bmp")
print("CBC Done")
