import rsa
import base64
from urllib import request
PRIVATE_FILE_PATH="private.pem"

def rsa_decrypt(code):
    code = request.unquote(code)
    with open(PRIVATE_FILE_PATH, 'rb') as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    code = base64.b64decode(code.encode('utf-8'))
    msg = rsa.decrypt(code, private_key).decode('utf-8')
    return msg

def rsa_sign(msg):
    with open(PRIVATE_FILE_PATH, 'rb') as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    signature = rsa.sign(msg, priv_key=private_key, hash_method='SHA-1')
    signature = base64.b64encode(signature)
    return bytes.decode(signature,encoding='utf-8')

