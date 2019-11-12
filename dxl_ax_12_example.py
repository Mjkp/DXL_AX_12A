import oscServer
import dxl_client_osc

'''
the aim of this code is to program the servo in readable way(clean page for control)
every dxl function has to be activated by Dispatcher exept port
'''

dxl_client_osc.portOpen()
#read position
oscServer.dispatch_callback("/readPosition",dxl_client_osc.positionRead)
#read load
oscServer.dispatch_callback("/readLoad",dxl_client_osc.loadRead)
#read temperature
oscServer.dispatch_callback("/readTemp",dxl_client_osc.tempRead)
#write torque
oscServer.dispatch_callback("/torque",dxl_client_osc.torqueEnable)
#write wheelmode
oscServer.dispatch_callback("/wheelMode",dxl_client_osc.wheelMode)
#write speed
oscServer.dispatch_callback("/writeSpeed",dxl_client_osc.servoSpeed)
#write goal position
oscServer.dispatch_callback("/writeGoalPos",dxl_client_osc.servoGoalPos)
#close port
oscServer.dispatch_callback("/closePort",dxl_client_osc.portClose)
#keep listening
oscServer.server_threading(oscServer.addr, oscServer.dispatcher)
