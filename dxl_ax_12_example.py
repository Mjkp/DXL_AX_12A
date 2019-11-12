import oscServer
import dxl_client_osc

'''
the aim of this code is to program the servo in readable way(clean page for control)
every dxl function has to be activated by Dispatcher exept port
'''

dxl_client_osc.portOpen()
#read position
oscServer.dispatch_callback("/readPosition",dxl_ax_12.positionRead)
#read load
oscServer.dispatch_callback("/readLoad",dxl_ax_12.loadRead)
#read temperature
oscServer.dispatch_callback("/readTemp",dxl_ax_12.tempRead)
#write torque
oscServer.dispatch_callback("/torque",dxl_ax_12.torqueEnable)
#write wheelmode
oscServer.dispatch_callback("/wheelMode",dxl_ax_12.wheelMode)
#write speed
oscServer.dispatch_callback("/writeSpeed",dxl_ax_12.servoSpeed)
#write goal position
oscServer.dispatch_callback("/writeGoalPos",dxl_ax_12.servoGoalPos)
#close port
oscServer.dispatch_callback("/closePort",dxl_ax_12.portClose)
#keep listening
oscServer.server_threading(oscServer.addr, oscServer.dispatcher)
