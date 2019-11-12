import os
from dynamixel_sdk import *
import oscClient
'''
This script is for dynamixel ax 12a control via OSC. It includes dynamixel sdk and python-osc udp_client
by Justin Moon 2019
'''
# Control table address
ADDR_AX_TORQUE_ENABLE      = 24
ADDR_AX_GOAL_POSITION      = 30
ADDR_AX_PRESENT_POSITION   = 36
ADDR_AX_MOVING_SPEED       = 32
ADDR_AX_PRESENT_LOAD       = 40
ADDR_AX_PRESENT_TEMPERATURE= 43
ADDR_AX_CW_ANGLE_LIMIT     = 6
ADDR_AX_CCW_ANGLE_LIMIT    = 8

# Protocol version
PROTOCOL_VERSION            = 1.0                           # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID_1                    = 1                             # Dynamixel ID : 1
DXL_ID_2                    = 2                             # Dynamixel ID : 2

DXL_IDs                     = (DXL_ID_1,DXL_ID_2)
BAUDRATE                    = 1000000                       # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'                # Check which port is being used on your controller
                                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                             # Value for enabling the torque
TORQUE_DISABLE              = 0                             # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 10                            # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1000                          # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                            # Dynamixel moving status threshold

angleLimit_r                = 0
angleLimit_l                = 1023
WHEEL_ENABLE                = 1
WHEEL_DISABLE               = 0
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)


def portOpen():
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        quit()
    setBaud()

def setBaud():
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        quit()

def portClose(_unused_pattern,_unused_msg):
    portHandler.closePort()

def split_msg(msg):
    id_and_value_str = msg.split("#")
    id_and_value = (id_and_value_str[0],id_and_value_str[1])
    return id_and_value

def torqueEnable(_unused_pattern,id_value):
    id, value = split_msg(id_value)
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_IDs[int(id)], ADDR_AX_TORQUE_ENABLE, int(value))
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def positionRead(_unused_pattern,_id):
    id = int(_id)
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_IDs[id], ADDR_AX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    oscClient.send_osc("/position_feedback", dxl_present_position)
    print("[ID:%03d]  PresPos:%03d" % (id, dxl_present_position))
    return dxl_present_position

def servoSpeed(_unused_pattern,id_value):
    id, value = split_msg(id_value)
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_IDs[int(id)], ADDR_AX_MOVING_SPEED, int(value))
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def wheelMode(_unused_pattern,id_boolean):
    id, boolean = split_msg(id_boolean)
    if int(boolean) == WHEEL_ENABLE:
        angleLimit_r =0
        angleLimit_l = 0
    elif int(boolean) == WHEEL_DISABLE :
        angleLimit_r = 0
        angleLimit_l = 1023

    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_IDs[int(id)], ADDR_AX_CW_ANGLE_LIMIT,angleLimit_r)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_IDs[int(id)], ADDR_AX_CCW_ANGLE_LIMIT,angleLimit_l)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def servoGoalPos(_unused_pattern,id_value):
    id, value = split_msg(id_value)
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_IDs[int(id)], ADDR_AX_GOAL_POSITION, int(value))
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def loadRead(_unused_pattern,_id):
    id = int(_id)
    dxl_present_load, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_IDs[id], ADDR_AX_PRESENT_LOAD)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    oscClient.send_osc("/load_feedback", dxl_present_load)
    print("[ID:%03d]  PresLoad:%03d" % (id, dxl_present_load))
    return dxl_present_load

def tempRead(_unused_pattern,_id):
    id = int(_id)
    dxl_present_temp, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_IDs[id], ADDR_AX_PRESENT_TEMPERATURE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    oscClient.send_osc("/temp_feedback", dxl_present_temp)
    print("[ID:%03d]  PresLoad:%03d" % (id, dxl_present_temp))
    return dxl_present_temp

#if __name__ == "__main__":
    # portOpen()
    # wheelMode(DXL_IDs[0],WHEEL_ENABLE)
    # servoSpeed(DXL_IDs[0],0)
    # split_msg("3#500")
    # torqueEnable("dd","0#0")
    # wheelMode("dd","0#1")
    # servoSpeed("dd","0#0")
    # torqueEnable("dd","1#1")
