import socket

'''
  Code for creating a socket for connecting to server.py
'''
serverIP = "10.0.1.2"
dst_ip = serverIP
s = socket.socket()
print(dst_ip)
port = 12346
s.connect((dst_ip, port))

#Write your code here:
#1. Add code to send HTTP GET / PUT / DELETE request. The request should also include KEY.
#2. Add the code to parse the response you get from the server.
# s.send('Hello server'.encode())
# print ('Client received '+s.recv(1024).decode())


'''
	Here we will wait for a request to be entered
	Once request is entered then we will send that request to the server
	and recieve the message from the server
'''
p = 1
k = 1
while(True):
	if p == 7:
		break
	inp = "GET /assignment1?request=key" + str(p) + " HTTP/1.1\r\n\r\n"
	k += 1
	if k == 4:
		p += 1
		k = 1
	#print("hai1")
	# variables for checking first three characters and the value is assignment1 or not
	request_type = inp[:3]
	basic_checking = inp[5:16]
	#print("hai2")
	# if the request is GET and the following text is assignment1
	# then only we sending message else just throw an error
	if(request_type == "GET" and basic_checking == "assignment1"):
		#print("hai3")
		s.send(inp.encode())
		message = s.recv(1024).decode()
		print('Client Received ' + message)
		if(message == "HTTP/1.1 200 OK\r\n\r\n"):
			message1 = s.recv(1024).decode()
			print('Client Received ' + message1)
	elif(request_type == "PUT" and basic_checking == "assignment1"):
		#print("hai4")
		s.send(inp.encode())
		message = s.recv(1024).decode()
		print('Client Received ' + message)
	elif(request_type == "DEL"):
		#print("hai5")
		request_type = inp[:6]
		basic_checking = inp[8:19]
		# the request will only be sent if and only it is DELETE
		if(request_type == "DELETE" and basic_checking == "assignment1"):
			s.send(inp.encode())
			message = s.recv(1024).decode()
			print('Client Received ' + message)
		else:
			print("400 Bad Request")
			continue
	else:
		#print("hai6")
		print("400 Bad Request")
		continue

	# message = s.recv(1024).decode()
	# print('Client Received ' + message)


s.close()
