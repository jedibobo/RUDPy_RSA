import rsa
import base64
from urllib import request
 
 
PUBLIC_FILE_PATH="public_pkcs8.pem"
PRIVATE_FILE_PATH="private.pem"
def rsa_encrypt(msg):
    with open(PUBLIC_FILE_PATH, 'rb') as public_file:
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_file.read())
    code = rsa.encrypt(msg.encode('utf-8'), public_key)
    code = base64.b64encode(code).decode('utf-8')
    #code = request.quote(code)
    return code
 
 
def rsa_decrypt(code):
    code = request.unquote(code)
    with open(PRIVATE_FILE_PATH, 'rb') as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    code = base64.b64decode(code.encode('utf-8'))
    msg = rsa.decrypt(code, private_key).decode('utf-8')
    return msg


# s = '12345678'
# print(s)
# s = rsa_encrypt(s)
# print(s)
# s = rsa_decrypt(s)
# print(s)