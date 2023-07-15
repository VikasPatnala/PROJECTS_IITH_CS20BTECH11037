import socket

#WRITE CODE HERE:
#1. Create a KEY-VALUE pairs (Create a dictionary OR Maintain a text file for KEY-VALUES).

'''
  Code for creating a socket for connecting to server.py
'''
serverIP = "10.0.1.3"
s1 = socket.socket()
#dst_ip = str(input("Enter dstIP: "))
dst_ip = "10.0.1.3"
port = 12345
s1.connect((dst_ip, port))

'''
  Code for creating a socket for connecting to client.py
'''
s2 = socket.socket()
print ("Socket successfully created")
#dst_ip = str(input("Enter Server IP: "))
dst_ip = "10.0.1.2"
dport = 12346
s2.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

'''
  s2 socket is listening for requests from client
'''
s2.listen(5)
print ("socket is listening")


# creating a empty dictionary for storing the key-value pair
dictionary = {}

# accepting the connection
c, addr = s2.accept()
print ('Got connection from', addr)

# recieving the message for the first time
recvmsg = c.recv(1024).decode()


'''
  while loop will traverse until we will don't
  receive any message
'''
while recvmsg:
  print('Cache received '+ recvmsg)

  request_type = recvmsg[:3]

  # if the request is GET
  if(request_type == "GET"):
    # code for just collecting the key from the request
    substr1 = "request="
    substr2 = " HTTP/1.1"

    index1 = recvmsg.find(substr1)
    index2 = recvmsg.find(substr2)

    key = recvmsg[index1 + len(substr1): index2]

    '''
      So First we are searching the key in the cache dictonary
        if we find in cache then just return that
        else request to the server and return the server message to the client
    '''
    if (dictionary.get(key) != None):
      buffer_text = "HTTP/1.1 200 OK\r\n\r\n";
      c.send(buffer_text.encode())
      val = dictionary[key]
      val = val + '\r\n\r\n'
      c.send(val.encode())
    else:
      s1.send(recvmsg.encode())
      val = s1.recv(1024).decode()
      if(val == "HTTP/1.1 404 Not Found\r\n\r\n"):
        c.send(val.encode())
      else:
        buffer_text = s1.recv(1024).decode()
        c.send(val.encode())
        dictionary[key] = buffer_text
        c.send(buffer_text.encode())
  elif(request_type == "PUT"):
    # code for just collecting the key and val from the request
    substr1 = "assignment1/"
    substr2 = " HTTP/1.1"

    index1 = recvmsg.find(substr1)
    index2 = recvmsg.find(substr2)

    key_value = recvmsg[index1 + len(substr1): index2]
    key_value_pair = key_value.split('/')

    key = key_value_pair[0]
    val = key_value_pair[1]

    '''
      Here no need for searching for because its a PUT request
      hence just store the key-value pair here and then also send a PUT request to the server
    '''
    dictionary[key] = val
    s1.send(recvmsg.encode())
    buffer_text = s1.recv(1024).decode()
    buffer_text = buffer_text + '\r\n\r\n'
    c.send(buffer_text.encode())
  elif(request_type == "DEL"):
    # code for just collecting the key which to is be deleted
    substr1 = "assignment1/"
    substr2 = " HTTP/1.1"

    index1 = recvmsg.find(substr1)
    index2 = recvmsg.find(substr2)

    key = recvmsg[index1 + len(substr1): index2]

    # if the cache dictionary doesn't contain the key then forward the request to server
    if (dictionary.get(key) != None):
      del dictionary[key]

    '''
      Here we are first deleting the key in the cache
      and then deleting the key in server
    '''
    s1.send(recvmsg.encode())
    buffer_text = s1.recv(1024).decode()
    buffer_text = buffer_text + '\r\n\r\n'
    c.send(buffer_text.encode())

  # recieving message
  recvmsg = c.recv(1024).decode()


  #c.send('Hello client'.encode())
  #Write your code here
  #1. Uncomment c.send
  #2. Parse the received HTTP request
  #3. Do the necessary operation depending upon whether it is GET, PUT or DELETE
  #4. Send response
  ##################


  #break
