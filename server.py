import socket
import threading
import hashlib
import time
import datetime
import random
# from RSAutils import RsaUtil
# rsa_codec=RsaUtil()
# from test_keys import rsa_encrypt
from encrypt import rsa_encrypt

# PLP Simulation settings
lossSimualation = False

# Set address and port
serverAddress = "localhost"
serverPort = 10000


# Delimiter
delimiter = "&|~|&~"

# Seq number flag
seqFlag = 0

# Packet class definition
class packet():
    def __init__(self):
        self.checksum = 0 
        self.length = 0 #length of 
        self.seqNo = 0 #number of sequence
        self.msg = 0 

    def make(self, data):
        self.msg = str(data)
        self.length = str(len(data))
        self.checksum=hashlib.sha1(data.encode("utf-8")).hexdigest()
        print("Length: %s\nSequence number: %s" % (self.length, self.seqNo))


# Connection handler
def handleConnection(address, data):
    drop_count=0
    packet_count=0
    time.sleep(0.5)
    if lossSimualation:
        packet_loss_percentage=float(input("Set PLP (0-99)%: "))/100.0
        while packet_loss_percentage<0 or packet_loss_percentage >= 1:
          packet_loss_percentage = float(input("Enter a valid PLP value. Set PLP (0-99)%: "))/100.0
    else:
        packet_loss_percentage = 0
    start_time=time.time()
    print("Request started at: " + str(datetime.datetime.utcnow()))
    pkt = packet()
    threadSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Read requested file
        data=bytes.decode(data,encoding='utf-8')
        print('file name:',data)
        try:
            print("Opening file %s" % data)
            fileRead = open(data, 'r')
            data = fileRead.read()
            #print('content',data)
            print(len(data))
            fileRead.close()
        except:
            msg="Found No File"
            pkt.make(msg)
            finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter + pkt.msg
            threadSock.sendto(finalPacket, address)
            print("Requested file could not be found, replied with FNF")
            

        # Fragment and send file 500 byte by 500 byte
        x = 0
        resend_count=0
        while x < (len(data) // 50) + 1:
            packet_count += 1
            randomised_plp = random.random()
            if packet_loss_percentage < randomised_plp:
                msg = data[x * 50:x * 50 + 50]
                #print('msg',msg)
                pkt.make(msg)

                finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter + pkt.msg
                # Send packet
                if len(finalPacket)==0:
                    break

                #encryption
                #finalPacket=rsa_codec.encrypt_by_public_key(finalPacket)
                print(finalPacket,"len:",len(finalPacket))
                encryption=rsa_encrypt(finalPacket)
                print("encryption",encryption)

                sent = threadSock.sendto(bytes(encryption,encoding='utf-8'), address)
                print('Sent %s bytes back to %s, awaiting acknowledgment..' % (sent, address))
                threadSock.settimeout(2)
                try:
                    ack, address = threadSock.recvfrom(100)
                    ack=bytes.decode(ack,encoding='utf-8')
                except:
                    print("Time out reached, resending ...%s" % x)
                    resend_count+=1
                    if resend_count>3:
                        print("Failed after 3 times of resending! Aborting!!!")
                        import sys
                        sys.exit(1)
                    else:
                        continue
                if ack.split(",")[0] == str(pkt.seqNo):
                    pkt.seqNo = int(not pkt.seqNo)
                    print("Acknowledged by: " + ack + "\nAcknowledged at: " + str(
                        datetime.datetime.utcnow()) + "\nElapsed: " + str(time.time() - start_time))
                    x += 1
            else:
                print("\n------------------------------\n\t\tDropped packet\n------------------------------\n")
                drop_count += 1
        print("Packets served: " + str(packet_count))
        if lossSimualation:
            print("Dropped packets: " + str(drop_count)+"\nComputed drop rate: %.2f" % float(float(drop_count)/float(packet_count)*100.0))
    except:
        print("Internal server error")



# Start - Connection initiation
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (serverAddress, serverPort)
print('Starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listening for requests indefinitely
while True:
    print('Waiting to receive message')
    data, address = sock.recvfrom(600)
    connectionThread = threading.Thread(target=handleConnection, args=(address, data))
    connectionThread.start()
    print('Received %s bytes from %s' % (len(data), address))