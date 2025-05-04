import urllib.request
import urllib.parse
import http.cookiejar
import json
import re

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

def send_code(phone):
    url = "https://my.telegram.org/auth/send_password"
    data = urllib.parse.urlencode({'phone': phone}).encode()
    req = urllib.request.Request(url, data=data)
    with opener.open(req) as response:
        try:
           result = json.loads(response.read().decode())
        except json.decoder.JSONDecodeError:
           raise Exception('This Number Is Limited')
        if "random_hash" in result:
            return result["random_hash"]
        raise Exception("Failed to send code By send_code()")

def login_number(phone, random_hash, code):
    url = "https://my.telegram.org/auth/login"
    data = urllib.parse.urlencode({
        'phone': phone,
        'random_hash': random_hash,
        'password': code
    }).encode()
    req = urllib.request.Request(url, data=data)
    with opener.open(req):
        for cookie in cookie_jar:
            if cookie.name == "stel_token":
                return cookie.value
        raise Exception("Login failed By login_number()")

def GetApis(phone=None,code=None):
    if phone:
       random_hash = send_code(phone)
    else:
       phone = input("Enter your phone number (e.g., +201234567890): ")
       random_hash = send_code(phone)
    if code:
        token = login_number(phone, random_hash, code)
    else:
        code = input("Enter your code (e.g., XmL56vx): ")
        token = login_number(phone, random_hash, code)
    url = "https://my.telegram.org/apps"
    req = urllib.request.Request(url)
    with opener.open(req) as response:
        html = response.read().decode()
        matches = re.findall(r'>(\w+)<', html)
        if (matches[5]).isdigit:
            dict_data = {
            'api_id': matches[5],
            'api_hash': matches[6]
            }
            return dict_data
        raise Exception("Error Getting Apis By GetApis()")
