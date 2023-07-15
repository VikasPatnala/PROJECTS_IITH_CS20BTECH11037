import socket
import time
import struct
import threading

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# socket_udp.settimeout(1)
window_size = 256
# curr_size = 0

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
#
# def Pack(sq, c):
#     packet = struct.pack(
#                 '!Hs',
#                 sq,
#                 bytes(c, 'utf-8')
#             )
#     return packet
#
# def UnPackAck(AckPacket):
#     sq, ack = struct.unpack('!Hs', AckPacket[0])
#     # print(sq, ack.decode())
#     return {sq, ack.decode()}
#
# def state2(sq, eof, data):
#     socket_udp.settimeout(0.005)
#     try:
#         AckPacket = socket_udp.recvfrom(bufferSize)
#         ack_sq = AckPacket[0].decode()
#         ack_sq = int(ack_sq)
#         # ack_sq, ack_mes = UnPackAck(AckPacket)
#     # print(ack_sq, ack_mes)
#     # print(type(ack_mes), type(ack_sq))
#     # print(ack_sq, ack_mes)
#         if(ack_sq != sq):
#             print("Hai")
#             state2(sq, eof, data)
#     except:
#         state1(sq, eof, data)
#
#
# def state1(sq, eof, data):
#     packet = struct.pack('!Hs', sq, bytes(eof, 'utf-8'))
#     # packet = Pack(sq, eof)
#     packet += data
#     socket_udp.sendto(packet, recieverAddressPort)
#     # state2(sq, eof, data)

print("Enter File Name: ")
fname = "testFile.jpg"
socket_udp.sendto(fname.encode(), recieverAddressPort)
img_data = [0]
img = open(fname, 'rb')
total_packets = 0
data = img.readline(1021)
while (data):
    img_data.append(data)
    data = img.readline(1021)
    total_packets += 1
    # print(data)
print(total_packets)

base_num = 1
next_seq_num = 1
ok = False

def recieving_thread():
    global base_num
    global next_seq_num
    global ok
    socket_udp.settimeout(0.005)
    while(True):
        try:
            packet = socket_udp.recvfrom(bufferSize)
            sq_num = packet[0].decode()
            # print(sq_num, type(sq_num))
            sq_num = int(sq_num)
            if(sq_num >= base_num):
                # print("Hai")
                base_num = sq_num + 1
                if(base_num >= total_packets or ok == True):
                    return
            # else:
            #     next_seq_num = base_num
        except:
            next_seq_num = base_num
    socket_udp.settimeout(None)

def sending_thread():
    global base_num
    global next_seq_num
    while(True):
        if(next_seq_num >= total_packets):
            ok = True
            print("hai")
            packet = struct.pack('!Hs', next_seq_num, b'e')
            socket_udp.sendto(packet, recieverAddressPort)
            break
        while(base_num < total_packets and next_seq_num < total_packets and next_seq_num < base_num + window_size):
            # if(base_num = len(data)):
            packet = struct.pack('!Hs', next_seq_num, b'n')
            packet += img_data[next_seq_num]
            try:
                socket_udp.sendto(packet, recieverAddressPort)
            except:
                socket_udp.sendto(packet, recieverAddressPort)
            next_seq_num += 1
            if(next_seq_num >= total_packets):
                break

if __name__ =="__main__":
    # global base_num
    # base_num = 1
    # global next_seq_num
    # next_seq_num = 1
    t1 = threading.Thread(target=sending_thread, args=())
    t2 = threading.Thread(target=recieving_thread, args=())
    start = time.time()
    t1.start()
    # time.sleep(1)
    t2.start()
    t1.join()
    end = time.time()
    time = (end - start)
    print(time)
    tp = 1144.83984375 / time
    print("Throughput is : ", tp)
    socket_udp.settimeout(None)
    msgFromServer = socket_udp.recvfrom(bufferSize)
    msgString = "Message from Server {}".format(msgFromServer[0])
    print(msgString)
    exit()

# flag = True
# start_seq = 0
#
# while(True):
#     if(next_seq_num >= 4816):
#         packet = struct.pack('!Hs', next_seq_num, b'e')
#         socket_udp.sendto(packet, recieverAddressPort)
#         break
#     if(flag):
#         while(next_seq_num < base_num + window_size):
#             packet = struct.pack('!Hs', next_seq_num, b'n')
#             packet += img_data[next_seq_num]
#             socket_udp.sendto(packet, recieverAddressPort)
#             next_seq_num += 1
#     socket_udp.settimeout(0.1)
#     try:
#         packet = socket_udp.recvfrom(bufferSize)
#         sq_num = packet[0].decode()
#         if(sq_num == base_num):
#             base = sq_num + 1
#             flag = True
#         else:
#             flag = False
#     except:
#         buffer = base_num
#         while(buffer < next_seq_num):
#             packet = struct.pack('!Hs', buffer, bytes('n', 'utf-8'))
#             packet += img_data[buffer]
#             socket_udp.sendto(packet, recieverAddressPort)



#
# while True:
#     while(curr_size != window_size):
#         state1(sq_num, 'n', strng)
#
#     strng = img.readline(1021)
#     if not strng:
#         packet = struct.pack('!Hs', sq_num, bytes('e', 'utf-8'))
#         sq_num += 1
#         packet += strng
#         socket_udp.sendto(packet, recieverAddressPort)
#         break
#     state1(sq_num, 'n', strng)
#     sq_num += 1
#     sq_num %= 2
#     # time.sleep(0.001)
