import hashlib

class packet():
    def __init__(self):
        self.checksum = 0 
        self.length = 0 #length of 
        self.seqNo = 0 #number of sequence
        self.msg = 0 
        print("init success")


    def make(self, data):
        self.msg = str(data)
        self.length = str(len(data))
        self.checksum=hashlib.sha1(data.encode("utf-8")).hexdigest()
        print("Length: %s\nSequence number: %s" % (self.length, self.seqNo))
        
test=packet()
test.make("this is a test~!!!!")
print(test.checksum)