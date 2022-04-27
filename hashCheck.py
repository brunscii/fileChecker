
def sha1(filename):
    sha1 = hashlib.sha1()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            sha1.update(data)
    print("SHA1: {0}".format(sha1.hexdigest()))
    
    return sha1.hexdigest()