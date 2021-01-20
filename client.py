import socket
import hashlib
import os
import time

#from test_keys import rsa_decrypt
from decrypt import rsa_decrypt

# Set address and port
serverAddress = "localhost"
serverPort = 10000

# Delimiter
delimiter = "&|~|&~"

# Start - Connection initiation
fsize = 0
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10)
    server_address = (serverAddress, serverPort)
    userInput = input("\nRequested file: ")
    fsize = os.path.getsize(userInput)
    message = userInput
    seqNoFlag = 0
    f = open("r_" + userInput, 'w')

    try:
        # Connection trials
        connection_trials_count=0
        # Send data
        print('Requesting %s' % message)
        
        sent = sock.sendto(bytes(message,encoding='utf-8'), server_address)
        # Receive indefinitely
        start=time.time()
        while True:
            # Receive response
            print('\nWaiting to receive..')
            try:
                data, server = sock.recvfrom(4096)
                # Reset failed trials on successful transmission
                connection_trials_count=0
            except:
                connection_trials_count += 1
                if connection_trials_count < 5:
                    print("\nConnection time out, retrying")
                    continue
                else:
                    print("\nMaximum connection trials reached, skipping request\n")
                    os.remove("r_" + userInput)
                    break
            data=bytes.decode(data,encoding='utf-8')
    
            #encryption 
            #data=rsa_codec.decrypt_by_private_key(data)

            seqNo = data.split(delimiter)[1]
            clientHash = hashlib.sha1(data.split(delimiter)[3].encode("utf-8")).hexdigest()
            print("Server hash: " + data.split(delimiter)[0])
            print("Client hash: " + clientHash)
            if data.split(delimiter)[0] == clientHash and seqNoFlag == int(seqNo == True):
                packetLength = data.split(delimiter)[2]
                if data.split(delimiter)[3] == "FNF":
                    print ("Requested file could not be found on the server")
                    os.remove("r_" + userInput)
                else:
                    f.write(data.split(delimiter)[3])
                print("Sequence number: %s\nLength: %s" % (seqNo, packetLength))
                print("Server: %s on port %s" % server)
                sent = sock.sendto(bytes(str(seqNo) + "," + packetLength,encoding='utf-8'), server)
            else:
                print("Checksum mismatch detected, dropping packet")
                print("Server: %s on port %s" % server)
                continue
            if int(packetLength) < 50:
                seqNo = int(not seqNo)
                break

    finally:
        end=time.time()
        print("speed:{}KB/s".format(fsize/1000/(end-start)))
        print("Closing socket")
        sock.close()
        f.close()