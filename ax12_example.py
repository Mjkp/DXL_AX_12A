from dxl_ax_12 import*
from pythonosc import udp_client

out_ip, out_port = "127.0.0.1",9998
client = udp_client.UDPClient(out_ip,out_port,False)
#client = SimpleUDPClient(out_ip,out_port)

msg = input()
client.send_message("/position", msg)



portOpen()
# Disable or Enable Dynamixel Torque
torqueEnable(DXL_IDs[0],TORQUE_DISABLE)

# Set to Wheel mode
wheelMode(DXL_IDs[0],WHEEL_DISABLE)

#while 1:
    # set goal position
servoWrite(DXL_IDs[0], 1000)
    # Write servoSpeed
    # servoSpeed(DXL_IDs[0], 400)
    # Read present position
servoRead(DXL_IDs[0])

portClose()
