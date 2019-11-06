import os
'''
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
'''
from dynamixel_sdk import *                    # Uses Dynamixel SDK library
# Control table address
ADDR_MX_TORQUE_ENABLE      = 24	               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MX_MOVING_SPEED       = 32
ADDR_MX_PRESENT_LOAD       = 40
ADDR_MX_CW_ANGLE_LIMIT     = 6
ADDR_MX_CCW_ANGLE_LIMIT    = 8

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID_1                    = 1               # Dynamixel ID : 1
DXL_ID_2                    = 2               # Dynamixel ID : 2

DXL_IDs                     = (DXL_ID_1,DXL_ID_2)
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM8'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 10           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)


# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()


# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_IDs[1], ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))


'''
while 1:
    # Read present position
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position[index], dxl_present_position))
'''
'''
# Set to Wheel mode
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,DXL_IDs[0], ADDR_MX_CW_ANGLE_LIMIT, 0)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

dxl_comm_result = packetHandler.write2ByteTxRx(portHandler,DXL_IDs[0], ADDR_MX_CCW_ANGLE_LIMIT, 0)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
'''

'''
# Change Dynamixel CW Angle Limit
  dxl_comm_result = packetHandler->write2ByteTxRx(portHandler, DXL_ID, AX_CW_ANGLE_LIMIT_L, 0, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS)
  {
    Serial.println(packetHandler->getTxRxResult(dxl_comm_result));
  }
  else if (dxl_error != 0)
  {
    Serial.println(packetHandler->getRxPacketError(dxl_error));
  }
  else
  {
    Serial.println("Dynamixel CW angle set to 0 successfully!");
  }

  // Change Dynamixel CCW Angle Limit
  Serial.println("Before AX_CCW_ANGLE_LIMIT_L"); Serial.flush();
  dxl_comm_result = packetHandler->write2ByteTxRx(portHandler, DXL_ID, AX_CCW_ANGLE_LIMIT_L, 0, &dxl_error);
  Serial.println("After AX_CCW_ANGLE_LIMIT_L"); Serial.flush();
  if (dxl_comm_result != COMM_SUCCESS)
  {
    Serial.println(packetHandler->getTxRxResult(dxl_comm_result));
  }
  else if (dxl_error != 0)
  {
    Serial.println(packetHandler->getRxPacketError(dxl_error));
  }
  else
  {
    Serial.println("Dynamixel CCW angle set to 0 successfully!");
  }
  Serial.flush();
'''

'''
# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_IDs[0], ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")
'''
while 1:

    # Write goal position
    # dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_IDs[0], ADDR_MX_GOAL_POSITION, dxl_goal_position[index])
    # if dxl_comm_result != COMM_SUCCESS:
    #     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #     print("%s" % packetHandler.getRxPacketError(dxl_error))
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_IDs[1], ADDR_MX_CW_ANGLE_LIMIT,0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_IDs[1], ADDR_MX_CCW_ANGLE_LIMIT,0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_IDs[1], ADDR_MX_MOVING_SPEED,0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


    while 1:
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_IDs[1], ADDR_MX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_IDs[1], dxl_goal_position[index], dxl_present_position))

        if not abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0

# Close port
portHandler.closePort()
