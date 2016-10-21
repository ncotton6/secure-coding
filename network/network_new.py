import time
import zlib
import json

myList = []

def send(index):
    # Sending the whole message as a json blob with the attributes time, data and index
    # so that we know in which order we can retrieve the data on the server side
    # We're doing this because of the downside caused by the UDP setup
    # 'text_60k, nothing but we are assuming the size of each packet to be 60kb'
    message = {
        "senttime": time.time(),
        "data": op('text_60k').text, 
        "index": index
    }

    myList.append(message)
    message = json.dumps(message).encode('utf-8')
    message = zlib.compress(message)
    op('udpout_from_master').sendBytes(message)

for i in range(100):
    send(i)

# Some basic code to echo the packet back, then
def receive(messageBytes):
    message = zlib.decompress(messageBytes)
    message = message.decode('utf-8')
    message = json.loads(message)
    for m in myList:
        if m['index'] == message['index']:
            receivetime = time.time()
            roundtrip = receivetime - message['senttime']
            op('table1').appendRow(['compress', roundtrip])
