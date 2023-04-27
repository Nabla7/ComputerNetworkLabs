import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('www.google.be', 80))
send_result = client.send(b'''GET / HTTP/1.0\r\n\r\n''')

complete_response = ''

resp = client.recv(512)

while resp != b'':
    complete_response += str(resp)
    resp = client.recv(512)

print(complete_response)