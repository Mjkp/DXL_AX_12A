/*
 * Dynamixel : AX-series with Protocol 1.0
 * Controller : OpenCM9.04C + OpenCM 485 EXP
 * Power Source : SMPS 12V 5A
 * 
 * AX-Series are connected to Dynamixel BUS on OpenCM 485 EXP board or DXL TTL connectors on OpenCM9.04
 * http://emanual.robotis.com/docs/en/parts/controller/opencm485exp/#layout
 * 
 * This example will test only one Dynamixel at a time.
*/

#include <DynamixelSDK.h>

// AX-series Control table address
#define ADDR_AX_TORQUE_ENABLE           24                 // Control table address is different in Dynamixel model
#define ADDR_AX_GOAL_POSITION           30
#define ADDR_AX_PRESENT_POSITION        36
#define ADDR_AX_LED_ENABLE              25

// Protocol version
#define PROTOCOL_VERSION                1.0                 // See which protocol version is used in the Dynamixel

// Default setting
#define DXL_ID                          2                   // Dynamixel ID: 1
#define BAUDRATE                        1000000
#define DEVICENAME                      "1"                 //DEVICENAME "1" -> Serial1(OpenCM9.04 DXL TTL Ports)
                                                            //DEVICENAME "2" -> Serial2
                                                            //DEVICENAME "3" -> Serial3(OpenCM 485 EXP)
#define TORQUE_ENABLE                   1                   // Value for enabling the torque
#define TORQUE_DISABLE                  0                   // Value for disabling the torque
#define LED_ENABLE                      1
#define LED_DISABLE                      0
#define DXL_MINIMUM_POSITION_VALUE      100                 // Dynamixel will rotate between this value
#define DXL_MAXIMUM_POSITION_VALUE      1000                // and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
#define DXL_MOVING_STATUS_THRESHOLD     20                  // Dynamixel moving status threshold

#define ESC_ASCII_VALUE                 0x1b

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while(!Serial);


  Serial.println("Start..");


  // Initialize PortHandler instance
  // Set the port path
  // Get methods and members of PortHandlerLinux or PortHandlerWindows
  dynamixel::PortHandler *portHandler = dynamixel::PortHandler::getPortHandler(DEVICENAME);

  // Initialize PacketHandler instance
  // Set the protocol version
  // Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
  dynamixel::PacketHandler *packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);

  int index = 0;
  int dxl_comm_result = COMM_TX_FAIL;             // Communication result
  int dxl_goal_position[2] = {DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE};         // Goal position

  uint8_t dxl_error = 0;                          // Dynamixel error
  int16_t dxl_present_position = 0;               // Present position

  // Open port
  if (portHandler->openPort())
  {
    Serial.print("Succeeded to open the port!\n");
  }
  else
  {
    Serial.print("Failed to open the port!\n");
    Serial.print("Press any key to terminate...\n");
    return;
  }

  // Set port baudrate
  if (portHandler->setBaudRate(BAUDRATE))
  {
    Serial.print("Succeeded to change the baudrate!\n");
  }
  else
  {
    Serial.print("Failed to change the baudrate!\n");
    Serial.print("Press any key to terminate...\n");
    return;
  }

  // Enable Dynamixel Torque
  dxl_comm_result = packetHandler->write1ByteTxRx(portHandler, DXL_ID, ADDR_AX_TORQUE_ENABLE, TORQUE_ENABLE, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS)
  {
    packetHandler->getTxRxResult(dxl_comm_result);
  }
  else if (dxl_error != 0)
  {
    packetHandler->getRxPacketError(dxl_error);
  }
  else
  {
    Serial.print("Dynamixel has been successfully connected \n");
  }

  
  // Enable Dynamixel Torque
  dxl_comm_result = packetHandler->write1ByteTxRx(portHandler, DXL_ID, ADDR_AX_LED_ENABLE, LED_ENABLE, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS)
  {
    packetHandler->getTxRxResult(dxl_comm_result);
    packetHandler->getRxPacketError(dxl_error);
    Serial.println("error writing to servo");
    Serial.print("dxl_error = ");
    Serial.println(dxl_error);
  }
  else
  {
    Serial.print("Dynamixel has LED on \n");
  }
  if (dxl_error != 0)
  {
    packetHandler->getRxPacketError(dxl_error);
    Serial.print("error ");
      Serial.println(dxl_error);
  }

  delay(10000);

  // Disable Dynamixel Torque
  dxl_comm_result = packetHandler->write1ByteTxRx(portHandler, DXL_ID, ADDR_AX_LED_ENABLE, LED_ENABLE, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS)
  {
    packetHandler->getTxRxResult(dxl_comm_result);
  }
  else if (dxl_error != 0)
  {
    packetHandler->getRxPacketError(dxl_error);
  }
  else
  {
    Serial.print("Dynamixel has LED off \n");
  }

  Serial.println("writing goal position");

  
    // Write goal position
    dxl_comm_result = packetHandler->write2ByteTxRx(portHandler, DXL_ID, ADDR_AX_GOAL_POSITION, DXL_MINIMUM_POSITION_VALUE, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS)
    {
      packetHandler->getTxRxResult(dxl_comm_result);
      Serial.println("error writing to servo");
    }
    if (dxl_error != 0)
    {
      packetHandler->getRxPacketError(dxl_error);
      Serial.print("error ");
      Serial.println(dxl_error);
    }

    delay(3000);

    // Write goal position
    dxl_comm_result = packetHandler->write2ByteTxRx(portHandler, DXL_ID, ADDR_AX_GOAL_POSITION, DXL_MAXIMUM_POSITION_VALUE, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS)
    {
      packetHandler->getTxRxResult(dxl_comm_result);
      Serial.println("error writing to servo");
    }
    if (dxl_error != 0)
    {
      packetHandler->getRxPacketError(dxl_error);
      Serial.print("error ");
      Serial.println(dxl_error);
    }


//  while(1)
//  {
//    Serial.print("Press any key to continue! (or press q to quit!)\n");
//
//
//    while(Serial.available()==0);
//
//    int ch;
//
//    ch = Serial.read();
//    if( ch == 'q' )
//      break;
//
//    // Write goal position
//    dxl_comm_result = packetHandler->write2ByteTxRx(portHandler, DXL_ID, ADDR_AX_GOAL_POSITION, dxl_goal_position[index], &dxl_error);
//    if (dxl_comm_result != COMM_SUCCESS)
//    {
//      packetHandler->getTxRxResult(dxl_comm_result);
//    }
//    else if (dxl_error != 0)
//    {
//      packetHandler->getRxPacketError(dxl_error);
//    }
//
////    do
////    {
////      // Read present position
////      dxl_comm_result = packetHandler->read2ByteTxRx(portHandler, DXL_ID, ADDR_AX_PRESENT_POSITION, (uint16_t*)&dxl_present_position, &dxl_error);
////      if (dxl_comm_result != COMM_SUCCESS)
////      {
////        packetHandler->getTxRxResult(dxl_comm_result);
////      }
////      else if (dxl_error != 0)
////      {
////        packetHandler->getRxPacketError(dxl_error);
////      }
////
////      Serial.print("[ID:");      Serial.print(DXL_ID);
////      Serial.print(" GoalPos:"); Serial.print(dxl_goal_position[index]);
////      Serial.print(" PresPos:");  Serial.print(dxl_present_position);
////      Serial.println(" ");
////
////
////    }while((abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD));
//
//    // Change goal position
//    if (index == 0)
//    {
//      index = 1;
//    }
//    else
//    {
//      index = 0;
//    }
//
//    delay(1000);
//  }
//
  // Disable Dynamixel Torque
  dxl_comm_result = packetHandler->write1ByteTxRx(portHandler, DXL_ID, ADDR_AX_TORQUE_ENABLE, TORQUE_DISABLE, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS)
  {
    packetHandler->getTxRxResult(dxl_comm_result);
  }
  else if (dxl_error != 0)
  {
    packetHandler->getRxPacketError(dxl_error);
  }

  // Close port
  portHandler->closePort();

}

void loop() {
  // put your main code here, to run repeatedly:
//  if(Serial.available() > 0){
//    char input = Serial.read();
//    if(input == 'q'){
//      portHandler->closePort();
//    }
//    }
//  }
}
