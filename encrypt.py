import rsa
import base64
from urllib import request
 
b_delimiter = b"&|~|&~"

PUBLIC_FILE_PATH="public_pkcs8.pem"
def rsa_encrypt(msg):
    with open(PUBLIC_FILE_PATH, 'rb') as public_file:
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_file.read())
    code = rsa.encrypt(msg.encode('utf-8'), public_key)
    code = base64.b64encode(code).decode('utf-8')
    #code = request.quote(code)
    return code

def rsa_verify(msg,signature):
    with open(PUBLIC_FILE_PATH, 'rb') as public_file:
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_file.read())
    signature = base64.b64decode(signature)
    return rsa.verify(msg, signature, public_key)
