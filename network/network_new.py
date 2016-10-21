import time
import zlib
import json

__author__ = "Praful Konduru"
__email__ = "pk5106@g.rit.edu"

# This serves as a persistent storage, to retreive message on way back.
# We can directly append the text we are sending to this structure
parent().store('messages', [])

def send(index):
    # Sending the whole message as a json blob with the attributes time, data and index
    # so that we know in which order we can retrieve the data on the server side
    # We're doing this because of the downside caused by the UDP setup
    message = {
        "senttime": time.time(),
        "data": op('text_60k').text, 
        "index": index
    }

    parent().fetch('messages').append(message)
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

    messages = parent().fetch('messages')
    for m in messages:
        if m['index'] == message['index']:
            receivetime = time.time()
            roundtrip = receivetime - message['senttime']
            op('table1').appendRow(['compress', roundtrip])
