from  pythonosc import udp_client

out_ip, out_port = "127.0.0.1",9998
client = udp_client.SimpleUDPClient(out_ip,out_port)

def send_osc(pattern,value):
    # distinguish the id of servo by msg
    client.send_message(pattern,value)
    print('sent value: {} pattern: {} to {}'.format(value,pattern,out_ip))

if __name__ == '__main__':
    terminal_input = input()
    pattern_msg = terminal_input.split("#")
    send_osc(pattern_msg[0],pattern_msg[1])
