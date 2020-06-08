#!/usr/bin/python

import base64, zlib

session_cookie = '.eJw9jU0OgjAQha9CZt2FUZCEE3gHNWRoR6iUjpm2siDc3WHj6st7eT8b2CJCMUMXSwgGPpySHwJBdwfLgQUMTCSseDE7hUVZcCZ4GhA_Trm3XI7-yUBJJL3DjNBtUOVj441f9EftXLdNe2nq5gpGo0MopO7K0ZFUKy8YVd5UotIVOyvS4vP0iPDcNSkcx__X_gP2ODvA.Eb00iw.7EBERatuwPNF_taGrxtqyp0s8HU'
data = session_cookie.split('.')[1]   # extract the payload
data += b'=' * ((4 - len(data) % 4))  # missing padding fix
data = base64.urlsafe_b64decode(data) # base64 decode
data = zlib.decompress(data)          # zlib decompress
print(data)
