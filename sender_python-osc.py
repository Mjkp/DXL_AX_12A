from  pythonosc import udp_client

ip,port = "127.0.0.1",8888

client = udp_client.SimpleUDPClient(ip,port)

msg = input()
client.send_message("/position", msg)
print('sent {} to {}'.format(msg,ip))
