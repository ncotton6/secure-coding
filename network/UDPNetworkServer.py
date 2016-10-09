import socket
import sys

HOST = '192.168.1.121' # this is the IP for my computer, we can change it if we want another computer to be the server
PORT = 5005

try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error as msg :
    print("Failed to create socket. Error Code : " + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()



try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

#now keep talking with the client
while 1:
    # receive dat from client (data, addr)
    data, addr = s.recvfrom(1024)
    if not data:
        break
    print("client send : ", data)
    reply = input('Enter message to reply :')

    s.sendto(reply , addr)
    print('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip())

s.close()
