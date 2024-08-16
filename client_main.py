from client import Client

client = Client('127.0.0.1', 12345)
client.send_file('file.txt')
