# generate pkcs8 format public key using private key

openssl rsa -in private.pem -pubout -out public_pkcs8.pem