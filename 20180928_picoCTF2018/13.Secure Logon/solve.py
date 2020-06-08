#!/usr/bin/env python3

import base64

cookie = 'cBF0Sy9OsxO6AYVi6pyNdlLEq2W00/dsqkHeaInulF1oSwXhfUjO0zFu2nhoCy4NDEG1i+zTMBxvPIWdcBfNow=='

print(cookie)
print()

decode = base64.b64decode(cookie)

flipped = bytes([decode[10] ^ ord('0') ^ ord('1')])

flipped_arr = []
for i in range(len(decode)):
    if i != 10:
        flipped_arr.append(bytes([decode[i]]))
    else:
        flipped_arr.append(flipped)

final = b''.join(flipped_arr)
print(base64.b64encode(final))
