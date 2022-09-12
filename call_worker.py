import array
import hashlib
import json
import requests

hasher = hashlib.sha512()
salt = "QueerBot"
#Hash the content dictionary with the password
def auth_hash(contents,password):
    content = ""
    for i in sorted(contents):
        content+= contents[i]
    hasher.update(bytes(content+salt+password,"utf-8"))
    hashbytes = hasher.digest()
    hasharr = array.array("B")
    hasharr.frombytes(hashbytes)
    hash = "{"
    for i in range(len(hasharr)):
        hash+= '"'+str(i)+'":'+str(hasharr[i])+","
    hash = hash[:-1]+"}"
    return hash

#content: Dictionary containing all the content you want to transmit
#password: the password
#url: the url to send to
async def call_bot_worker(content, password, url):
    hdrs = {"content-type": "application/json"}
    auth = auth_hash(content,password)
    content["hash"]=auth
    payload = json.dumps(content)
    
    try:
        r = requests.post(url=url, headers=hdrs, data=payload)
    except Exception:
        print(Exception)
    return r.text
