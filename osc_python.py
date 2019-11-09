from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

class Osc:
    def __init__(self,out_ip,out_port):
        self.out_ip = out_ip
        self.out_port = out_port
        self.client = udp_client.SimpleUDPClient(self.ip,self.port)

    def send_msg(self,pattern,msg):
        self.pattern = pattern
        self.msg = msg
        self.client.send_message(self.pattern,self.msg)
        print('sent {} to {}'.format(msg,ip))

    def recieve_msg(self, pattern, function):
        self.pattern = pattern
        function = function
        self.dispatch = dispatcher.Dispatcher()
        self.dispatch.map(self.pattern, self.function)
        addr=("0.0.0.0", 5000)

        server = osc_server.ForkingOSCUDPServer(addr,dispatch)
        server.serve_forever()




def position_func(addr,msg):
    print(addr,msg)

dispatch = dispatcher.Dispatcher()
dispatch.map("/position", position_func)

addr=("0.0.0.0", 5000)

server = osc_server.ForkingOSCUDPServer(addr,dispatch)
server.serve_forever()
