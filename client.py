
import time
import socket
import sys
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import ARC4

print('Client Server...')
time.sleep(1)
# Get the hostname, IP Address from socket and set Port
soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
# get information to connect with the server 
print(shost, '({})'.format(ip))
server_host = input('Enter server\'s IP address:')
name = input('Enter Client\'s name: ')
port = 1234
print('Trying to connect to the server: {}, ({})'.format(server_host, port))
time.sleep(1)
soc.connect((server_host, port))
print("Connected...\n")
soc.send(name.encode())
timer = False
delta = 0
server_name = soc.recv(1048576)
server_name = server_name.decode()
iv = b"Y\r*c'\x9b\x06u\x03X\xb7%F\xb6Yi"
print('{} has joined...'.format(server_name))
print('Enter [bye] to exit.')
while True:
    message = soc.recv(1048576)
    message = message.decode()
    print(server_name, ">", message)
    message = input(str("Me > "))
    if message[0] == '!':
        if message[1:] == "bye":
            soc.send(message.encode())
            print("\n")
            break
        else:
            arg = message.split(' ')
            delta = time.time()
            timer = True
            if arg[0] == '!rc4':
                input_file = open(arg[1], 'rb')
                input_data = input_file.read()
                cfb_cipher = ARC4.new(arg[2])
                message = '!rc4'+str(cfb_cipher.encrypt(input_data))
                with open('key.txt', 'w') as f:
                    f.write(arg[2])
            elif arg[0] == '!des':
                input_file = open(arg[1], 'rb')
                input_data = input_file.read()
                
                while len(input_data) % 8 != 0:
                    input_data += bytes('@', 'utf-8')
                cfb_cipher = DES.new(arg[2])
                with open('key.txt', 'w') as f:
                    f.write(arg[2])
                message = '!des'+str(cfb_cipher.encrypt(input_data))
            elif arg[0] == '!aes':
                input_file = open(arg[1], 'rb')
                input_data = input_file.read()
                cfb_cipher = AES.new(arg[2], AES.MODE_CFB, iv)
                message = '!aes'+str(cfb_cipher.encrypt(input_data))
                with open('key.txt', 'w') as f:
                    f.write(arg[2])
            else:
                print('Incorrect Command!\n')
                message = 'Hi,'
                timer = False
                delta = 0
    soc.send(message.encode())
    if(timer):
        delta = time.time()-delta
        delta_dec = soc.recv(1048576)
        delta_dec = float(delta_dec.decode())
        print('time taken on client side: ', delta)
        print('time taken on server side: ', delta_dec)
        print('total time: ', delta+delta_dec)
        timer = False
        delta = 0
