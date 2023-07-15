import socket

#WRITE CODE HERE:
#1. Create a KEY-VALUE pairs (Create a dictionary OR Maintain a text file for KEY-VALUES).

'''
  Code for creating a socket for connecting to client.py
'''
dst_ip = str(input("Enter Server IP: "))
s = socket.socket()
print ("Socket successfully created")
dport = 12346
s.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

'''
  s socket is listening for requests from cache
'''

s.listen(5)
print ("socket is listening")

# creating a dictionary with 6 initial key-value pair
dictionary = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3', 'key4': 'val4',  'key5': 'val5', 'key6': 'val6'}

# accepting the connection
c, addr = s.accept()

# recieving the message for the first time
print ('Got connection from', addr )
recvmsg = c.recv(1024).decode()


'''
  while loop will traverse until we will don't
  receive any message
'''
while recvmsg:
  print('Server received '+ recvmsg)

  request_type = recvmsg[:3]

  # if the request type is get
  if(request_type == "GET"):
    # code for just collecting the key from the request
    substr1 = "request="
    substr2 = " HTTP/1.1"

    index1 = recvmsg.find(substr1)
    index2 = recvmsg.find(substr2)

    key = recvmsg[index1 + len(substr1): index2]

    # checking wether the key value is present in the dictionary or not
    # if not then just throw an error
    if(dictionary.get(key) != None):
      val = dictionary[key]
      val = val + '\r\n\r\n'
      c.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
      c.send(val.encode())
    else:
      c.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
  elif(request_type == "PUT"):
    # code for just collecting the key and val pair from the request
    substr1 = "assignment1/"
    substr2 = " HTTP/1.1"

    index1 = recvmsg.find(substr1)
    index2 = recvmsg.find(substr2)

    key_value = recvmsg[index1 + len(substr1): index2]
    key_value_pair = key_value.split('/')

    key = key_value_pair[0]
    val = key_value_pair[1]

    # key-value pair is directly added here
    dictionary[key] = val
    c.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
  elif(request_type == "DEL"):
    # code for just collecting the key which is to be deleted
    substr1 = "assignment1/"
    substr2 = " HTTP/1.1"

    index1 = recvmsg.find(substr1)
    index2 = recvmsg.find(substr2)

    key = recvmsg[index1 + len(substr1): index2]

    # checking whether the key is already in dictionary or not
    # if not throwing an error to client
    if(dictionary.get(key) != None):
      del dictionary[key]
      c.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
    else:
      c.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
  else:
    c.send('HTTP/1.1 400 Bad Request\r\n\r\n'.encode())
  # recieving a message
  recvmsg = c.recv(1024).decode()
  #c.send('Hello client'.encode())


  #Write your code here
  #1. Uncomment c.send
  #2. Parse the received HTTP request
  #3. Do the necessary operation depending upon whether it is GET, PUT or DELETE
  #4. Send response
  ##################


  #break
