import os
from dynamixel_sdk import *
from datetime import datetime

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132
LEN_PRO_GOAL_POSITION       = 4
LEN_PRO_PRESENT_POSITION    = 4
COMM_SUCCESS                = 0

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
#DXL1_ID                     = 21
#DXL2_ID                     = 24
#DXL3_ID                     = 25

DXL1_ID                     = 25
DXL2_ID                     = 14


ROBOT_1_IDS                 = (DXL1_ID,DXL2_ID)
#ROBOT_2_IDS                 = (DXL4_ID,DXL5_ID,DXL6_ID)

BAUDRATE                    =  1000000        # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/tty.usbserial-FT2H2ZCB'   # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1
TORQUE_DISABLE              = 0

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION)
groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)

robot1Positions = []
#robot2Positions = []

isRecording1 = False
#isRecording2 = False

isPlaying1 = False
#isPlaying2 = False

recordRobot1Value = op('/project1/recordRobot1Value')
#recordRobot2Value = op('/project1/recordRobot2Value')

# table for robot 1 playback
robot1DataPlayback = op('/project1/robot1DataPlayback')
#robot2DataPlayback = op('/project1/robot2DataPlayback')

robot1CurrentFrame = 0
#robot2CurrentFrame = 0

def turnOn():
    setupSerial()
    torqueEnableAll(TORQUE_DISABLE)

def turnOff():
    print("closeSerial")
    closeSerial()

def setupSerial():
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")


    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")

def closeSerial():
    portHandler.closePort()

def torqueEnable(id, value):
    try:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, id, ADDR_PRO_TORQUE_ENABLE, value)
        if dxl_error:
            print(dxl_error)
            return False
        if dxl_comm_result != COMM_SUCCESS:
            print("status NOT OK for servoID",id,'status',dxl_comm_result)
            return False
    except Exception as e:
        print(e)
        return False
    return True

def torqueEnableTuple(ids,value):
    for servoID in ids:
        while not torqueEnable(servoID,value):
            print('trying to control torque for id',servoID)

def torqueEnableAll(value):
    torqueEnableTuple(ROBOT_1_IDS,value)
    #torqueEnableTuple(ROBOT_2_IDS,value)

def servoRead(id):
    try:
        position,dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler,id, ADDR_PRO_PRESENT_POSITION)
        if dxl_error:
            print(dxl_error)
            return (False,0)
        if dxl_comm_result != COMM_SUCCESS:
            print("status NOT OK for servoID",id,'status',dxl_comm_result)
            return (False,0)
    except Exception as e:
        print(e)
        return (False,0)
    return (True,position)

def servoWrite(id,value):
    if(value < 0):  value = 0
    if(value > 4095):   value = 4095

    try:
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler,id, ADDR_PRO_GOAL_POSITION,value)
        if dxl_error:
            #print("dxl_error",dxl_error)
            return False
        if dxl_comm_result != COMM_SUCCESS:
            #print("status NOT OK for servoID",id,'status',dxl_comm_result)
            return False
    except Exception as e:
        #print(e)
        return False
    return True

def appendRobotValues(ids,robotPositions):
    # TODO: check wiring!
    # -1 means position is invalid
    positionsToAppend = [-1,-1]
    index = 0
    # for each servo ID
    for id in ids:
        readOK, position = servoRead(id)
        # if we could correctly get data form the servo, store that in the right place with the 3 element tuple
        if readOK:
            positionsToAppend[index] = position
        index += 1
    # check if tha data is valid
    if positionsToAppend[0] != -1 and positionsToAppend[1] != -1 :
        robotPositions.append(positionsToAppend)
        print(len(robotPositions))

def sendValuesToRecorderOut(whichRobot,robotPositions):
    #print(len(robotPositions))
    t = op('/project1/robot'+str(whichRobot)+'Data')
    t.clear()

    for row in robotPositions:
        t.appendRow(row)

    robotPositions.clear()

def clearPositions(robotPositions):
    robotPositions.clear()

def offToOn(panelValue):
    return


def isValidPosition(value):
    return value >= 0 and value <= 4095

def incrementFileNameAndSaveTable(robotIndex):
    print('incrementFileNameAndSaveTable')
    # get the right reference to the list of recordings based on the robotindex
    if(robotIndex == 1):    robotPositions = robot1Positions
    #elif(robotIndex == 2):    robotPositions = robot2Positions
    else:   print("invalid robot index, can only be 1 or 2")
    # copy values to table
    sendValuesToRecorderOut(robotIndex,robotPositions)
    # save
    timestamp = str(datetime.now()).replace(' ','_').replace(':','-')
    timestamp = timestamp[0:timestamp.index('.')]
    filename = 'BehaviorData/Robot'+str(robotIndex)+'/'+timestamp+'_test.txt'
    op('recorderOutRobot'+str(robotIndex)).par.write.pulse()
    op ('recorderOutRobot'+str(robotIndex)).save(filename)
    print('saved','BehaviorData/Robot'+str(robotIndex)+'/'+timestamp+'_test.txt')

def resetAnimation(robotIndex):
    global robot1CurrentFrame
    if robotIndex == 1:
        robot1CurrentFrame = 0
    #if robotIndex == 2:
     #   robot2CurrentFrame = 0

def whileOn(panelValue):
    global robot1CurrentFrame
    if isRecording1:
        appendRobotValues(ROBOT_1_IDS,robot1Positions)
    #if isRecording2:
     #   appendRobotValues(ROBOT_2_IDS,robot2Positions)
    if isPlaying1:
        # increment by 1 but also loop back to start of animation after last frame
        robot1CurrentFrame = (robot1CurrentFrame + 1) % robot1DataPlayback.numRows
       # print('robot1CurrentFrame',robot1CurrentFrame)
        for index in range(2):
            servoID = ROBOT_1_IDS[index]
            value   = robot1DataPlayback[robot1CurrentFrame,index]
            servoWrite(servoID,value)
        # stop at last frame
        # if robot1CurrentFrame < robot1DataPlayback.numRows - 1:
        #     robot1CurrentFrame += 1
    #if isPlaying2:
        #print('playing2')
        # increment by 1 but also loop back to start of animation after last frame
       # robot2CurrentFrame = (robot2CurrentFrame + 1) % robot2DataPlayback.numRows
        #print('robot2CurrentFrame',robot2CurrentFrame)
       # for index in range(3):
        #    servoID = ROBOT_2_IDS[index]
       #     value   = robot2DataPlayback[robot2CurrentFrame,index]
        #    servoWrite(servoID,value)

    return

def onToOff(panelValue):
    return

def whileOff(panelValue):
    return

def valueChange(panelValue):
    #print(panelValue)
    return
