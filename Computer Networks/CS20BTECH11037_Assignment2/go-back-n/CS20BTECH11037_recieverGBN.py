import socket
import time
import struct
import threading

recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size

# bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )

# while True:
#
#     #wait to recieve message from the server
#     bytesAddressPair = socket_udp.recvfrom(bufferSize)
#     print(bytesAddressPair) #print recieved message
#
#     #split the recieved tuple into variables
#     recievedMessage = bytesAddressPair[0]
#     senderAddress = bytesAddressPair[1]
#
#     #print them just for understanding
#     msgString = "Message from Client:{}".format(recievedMessage)
#     detailString  = "Client IP Address:{}".format(senderAddress)
#     print(msgString)
#     print(detailString)
#
#     # Sending a reply to client
#     message = str.encode("This is a reply message from the server")
#     socket_udp.sendto(message, senderAddress)
def Unpack(packet):
    sq, flag = struct.unpack('!Hs', packet)
    return {sq, flag.decode()}

def AckPacket(isack, sq):
    ackpack = struct.pack(
                    '!Hs',
                    sq,
                    b'a'
                )
    return ackpack

sq_num = 1

def state1(sq_num):
    packet = socket_udp.recvfrom(bufferSize)
    udp_header = (packet[0])[:3]
    strng = (packet[0])[3:]
    sq, flag = struct.unpack('!Hs', udp_header)
    flag = flag.decode()
    # sq, flag = Unpack(udp_header)
    # sq = int(sq)
    # print(sq_num, sq, flag)
    # print(type(sq), type(flag))
    if(flag == 'e'):
        return 'EOF'
    if(sq_num != sq):
        print("Hai")
        sq = sq_num - 1
        sq = str(sq)
        socket_udp.sendto(sq.encode(), senderAddress)
        return "NONE"
        # return state1(sq_num)
    else:
        sq = str(sq)
        socket_udp.sendto(sq.encode(), senderAddress)
        return strng



bytesAddressPair = socket_udp.recvfrom(bufferSize)
fname = bytesAddressPair[0]
senderAddress = bytesAddressPair[1]
msgString = "Message from Client:{}".format(fname)
#print(msgString)
fname = 'documents/'+fname.decode()
fp = open(fname, 'wb')


while True:
    data = state1(sq_num)
    if(data == 'EOF'):
        break;
    else:
        if(data != "NONE"):
            fp.write(data)
            sq_num += 1

fp.close()
print("Data Received successfully")
message = str.encode("Data Received successfully")
socket_udp.sendto(message, senderAddress)
