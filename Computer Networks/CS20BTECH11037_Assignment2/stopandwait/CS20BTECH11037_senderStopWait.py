import socket
import time
import struct

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# socket_udp.settimeout(1)


# while True:
#
#     # Send to server using created UDP socket
#     msg = input("Please enter message to send: ")
#     message = str.encode(msg)
#     socket_udp.sendto(message, recieverAddressPort)
#
#     #wait for reply message from reciever
#     msgFromServer = socket_udp.recvfrom(bufferSize)
#
#     msgString = "Message from Server {}".format(msgFromServer[0])
#     print(msgString)

def Pack(sq, c):
    packet = struct.pack(
                '!Hs',
                sq,
                bytes(c, 'utf-8')
            )
    return packet

def UnPackAck(AckPacket):
    sq, ack = struct.unpack('!Hs', AckPacket[0])
    # print(sq, ack.decode())
    return {sq, ack.decode()}

def state2(sq, eof, data):
    socket_udp.settimeout(0.005)
    try:
        AckPacket = socket_udp.recvfrom(bufferSize)
        ack_sq = AckPacket[0].decode()
        ack_sq = int(ack_sq)
        # ack_sq, ack_mes = UnPackAck(AckPacket)
    # print(ack_sq, ack_mes)
    # print(type(ack_mes), type(ack_sq))
    # print(ack_sq, ack_mes)
        if(ack_sq != sq):
            print("Hai")
            state2(sq, eof, data)
    except:
        state1(sq, eof, data)


def state1(sq, eof, data):
    packet = struct.pack('!Hs', sq, bytes(eof, 'utf-8'))
    # packet = Pack(sq, eof)
    packet += data
    socket_udp.sendto(packet, recieverAddressPort)
    state2(sq, eof, data)

print("Enter File Name: ")
fname = "testFile.jpg"
socket_udp.sendto(fname.encode(), recieverAddressPort)
img = open(fname, 'rb')
sq_num = 0
start = time.time();
retransmission = 0
while True:
    strng = img.readline(1021)
    if not strng:
        packet = struct.pack('!Hs', sq_num, bytes('e', 'utf-8'))
        sq_num += 1
        packet += strng
        socket_udp.sendto(packet, recieverAddressPort)
        break
    packet = struct.pack('!Hs', sq_num, bytes('u', 'utf-8'))
    packet += strng
    socket_udp.sendto(packet, recieverAddressPort)
    while True:
        socket_udp.settimeout(0.1)
        try:
            AckPacket = socket_udp.recvfrom(bufferSize)
            ack_sq = AckPacket[0].decode()
            ack_sq = int(ack_sq)
            # ack_sq, ack_mes = UnPackAck(AckPacket)
        # print(ack_sq, ack_mes)
        # print(type(ack_mes), type(ack_sq))
        # print(ack_sq, ack_mes)
            if(ack_sq == sq_num):
                sq_num += 1
                sq_num %= 2
                break
                #     socket_udp.sendto(packet, recieverAddressPort)
            # else:
        except:
            socket_udp.sendto(packet, recieverAddressPort)
            retransmission += 1
    # state1(sq_num, 'n', strng)
    # time.sleep(0.001)
end = time.time()
time = end - start
print(time)
print("Average number of retransmission: {}", retransmission)
tp = 1144.83984375 / time
print("Throughput: ", tp)

socket_udp.settimeout(None)

msgFromServer = socket_udp.recvfrom(bufferSize)
msgString = "Message from Server {}".format(msgFromServer[0])
print(msgString)
