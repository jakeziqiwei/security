import urllib.request
import base64
import binascii
from pymd5 import md5, padding

# You can use knowledge of this key to help you debug; feel free to
# change it. However, it should work with the unmodified file

# We will grade your submission with keys of length 128 to 256 bits
# (all multiples of 8).
hexkey = '9238479238749827923989879287323409812230498a'


KEY = binascii.unhexlify(hexkey)


def get_user_url(cnet):
    h = md5()
    msg = KEY + b'uname=' + cnet + b'&role=user'
    h.update(msg)
    digest = h.hexdigest()
    url = ("http://www.flickur.com/?api_tag={md5_digest}"
           "&uname={cnet}&role=user").format(md5_digest=digest,
                                             cnet=cnet.decode('utf-8'))
    response = bytes(url, 'utf-8')
    return response


def query_url(url):

    if not url.startswith(b'http://www.flickur.com/?'):
        return b'Invalid URL'

    params_strs = url.lstrip(b'http://www.flickur.com/?')
    ps = list(map(lambda x: x.split(b'='), params_strs.split(b'&')))
    params = {p[0]: p[1] for p in ps if len(p) >= 2}
    amp_index = params_strs.find(b'&')
    msg = KEY + params_strs[amp_index+1:]
    h = md5()
    h.update(msg)

    if h.hexdigest() == params[b'api_tag'].decode('utf-8'):
        if params[b'role'] == b'admin':
            return b"Admin Login Success"
        elif params[b'role'] == b'user':
            return b'Non-Admin User Login OK'
        else:
            return b'Invalid role'
    else:
        return b'Invalid token'


# Code below here will be run if you execute 'python3 TODO'.
# This code here won't be graded, and your code above shouldn't depend on it.
if __name__ == "__main__":
    exit()
