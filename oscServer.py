from pythonosc import dispatcher
from pythonosc import osc_server

addr = ("0.0.0.0",8888)
dispatcher = dispatcher.Dispatcher()

def dispatch_callback(pattern,function):
    dispatcher.map(pattern, function)

def server_threading(args,_dispatcher):
    server = osc_server.ThreadingOSCUDPServer((args[0], args[1]), _dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

if __name__ ==  "__main__":
    # dispatch_run("/position",position_func)
    dispatch_callback("/reply",send_osc)
    server_threading(addr, dispatcher)
