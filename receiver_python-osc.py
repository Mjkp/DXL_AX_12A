from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import*

def position_func(addr,msg):
    print(addr,msg)


dispatch = dispatcher.Dispatcher()
dispatch.map("/position", position_func)
