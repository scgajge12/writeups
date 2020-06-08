#!/usr/bin/python

import base64, zlib

session_cookie = '.eJwlz01qAzEMQOG7eJ2FJEu2nMsEWT-0FFqYSVald89AD_DBe7_tUUeeH-3-PF55a4_PaPfGlWVJOKMEMwfuxGFLREF8TDaaGJlsgHvpSIfqYqy-e6RSgHZF3KK-YkyACyIzWnV1hmXiC7MrgIqYzG2uFrTSuLMMlHZrfh71eP585ffV40lDKyo2Vvdi4JhkTimLnRSozKsWXu515vE_QbP9vQHyWj98.Eb45Rw.2E7fsQB1cpukW7JcF1g6EtrOSN0'
data = session_cookie.split('.')[1]
data += b'=' * ((4 - len(data) % 4))
data = base64.urlsafe_b64decode(data)
data = zlib.decompress(data)
print(data)
