# generate pkcs8 format public key using private key

openssl rsa -in private.pem -pubout -out public_pkcs8.pem



需要注意RSA加密明文的长度，因为![image-20210120204400114](C:\Users\15824\AppData\Roaming\Typora\typora-user-images\image-20210120204400114.png)

之后由于文本内部也有计算sha1值，所以只剩55字节供传输。