import time
import socket
import sys
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import ARC4

print('Setup Server...')
time.sleep(1)
# Get the hostname, IP Address from socket and set Port
soc = socket.socket()
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = 1234
soc.bind((host_name, port))
print(host_name, '({})'.format(ip))
name = input('Enter name: ')
soc.listen(1)  # Try to locate using socket
print('Waiting for incoming connections...')
connection, addr = soc.accept()
iv = b"Y\r*c'\x9b\x06u\x03X\xb7%F\xb6Yi"

print("Received connection from ", addr[0], "(", addr[1], ")\n")
print('Connection Established. Connected From: {}, ({})'.format(
    addr[0], addr[0]))
# get a connection from client side
client_name = connection.recv(1048576)
timer = False
delta = 0
client_name = client_name.decode()
print(client_name + ' has connected.')
print('Press [bye] to leave the chat room')
connection.send(name.encode())
while True:
    message = input('Me > ')
    if message == '!bye':
        message = 'Good Night...'
        connection.send(message.encode())
        print("\n")
        break
    connection.send(message.encode())
    message = connection.recv(1048576)
    message = message.decode()
    if message[0] == '!':
        enc = message[1:4]
        timer = True
        delta = time.time()
        if enc == 'rc4':
            input_data = bytes(message[4:], 'utf-8')
            key = ''
            with open('key.txt', 'r') as f:
                key = f.read()
            cfb_cipher = ARC4.new(key)
            image_data = cfb_cipher.decrypt(input_data)
            output_file = open('got_rc4.png', "wb")
            output_file.write(image_data)
            output_file.close()
        elif enc == 'des':
            input_data = bytes(message[4:], 'utf-8')
            key = ''
            with open('key.txt', 'r') as f:
                key = f.read()
            cfb_cipher = DES.new(key)
            while len(input_data) % 8 != 0:
                input_data += bytes('@', 'utf-8')
            image_data = cfb_cipher.decrypt(input_data)
            output_file = open('got_des.png', "wb")
            output_file.write(image_data)
            output_file.close()
        elif enc == 'aes':
            input_data = bytes(message[4:], 'utf-8')
            key = ''
            with open('key.txt', 'r') as f:
                key = f.read()
            cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
            image_data = cfb_cipher.decrypt(input_data)
            output_file = open('got_aes.png', "wb")
            output_file.write(image_data)
            output_file.close()
    print(client_name, '>', message)
    if(timer):
        delta = time.time() - delta
        message = str(delta)
        connection.send(message.encode())
        delta = 0
        timer = False
