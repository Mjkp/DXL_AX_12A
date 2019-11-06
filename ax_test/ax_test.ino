#include <DynamixelSDK.h>

/** EEPROM AREA **/
#define AX_MODEL_NUMBER_L           0
#define AX_MODEL_NUMBER_H           1
#define AX_VERSION                  2
#define AX_ID                       3
#define AX_BAUD_RATE                4
#define AX_RETURN_DELAY_TIME        5
#define AX_CW_ANGLE_LIMIT_L         6
#define AX_CW_ANGLE_LIMIT_H         7
#define AX_CCW_ANGLE_LIMIT_L        8
#define AX_CCW_ANGLE_LIMIT_H        9
#define AX_SYSTEM_DATA2             10
#define AX_LIMIT_TEMPERATURE        11
#define AX_DOWN_LIMIT_VOLTAGE       12
#define AX_UP_LIMIT_VOLTAGE         13
#define AX_MAX_TORQUE_L             14
#define AX_MAX_TORQUE_H             15
#define AX_RETURN_LEVEL             16
#define AX_ALARM_LED                17
#define AX_ALARM_SHUTDOWN           18

/** RAM AREA **/
#define AX_TORQUE_ENABLE            24
#define AX_LED                      25
#define AX_CW_COMPLIANCE_MARGIN     26
#define AX_CCW_COMPLIANCE_MARGIN    27
#define AX_CW_COMPLIANCE_SLOPE      28
#define AX_CCW_COMPLIANCE_SLOPE     29
#define AX_GOAL_POSITION_L          30
#define AX_GOAL_POSITION_H          31
#define AX_GOAL_SPEED_L             32
#define AX_GOAL_SPEED_H             33
#define AX_TORQUE_LIMIT_L           34
#define AX_TORQUE_LIMIT_H           35
#define AX_PRESENT_POSITION_L       36
#define AX_PRESENT_POSITION_H       37
#define AX_PRESENT_SPEED_L          38
#define AX_PRESENT_SPEED_H          39
#define AX_PRESENT_LOAD_L           40
#define AX_PRESENT_LOAD_H           41
#define AX_PRESENT_VOLTAGE          42
#define AX_PRESENT_TEMPERATURE      43
#define AX_REGISTERED_INSTRUCTION   44
#define AX_PAUSE_TIME               45
#define AX_MOVING                   46
#define AX_LOCK                     47
#define AX_PUNCH_L                  48
#define AX_PUNCH_H                  49

// Protocol version
#define PROTOCOL_VERSION                1.0

// Default setting
#define DXL_ID                          254                // Dynamixel ID: 1
#define BAUDRATE                        1000000
#define DEVICENAME                      "3"                 // Check which port is being used on your controller

#define TORQUE_ENABLE                   1                   // Value for enabling the torque
#define TORQUE_DISABLE                  0                   // Value for disabling the torque

#define ESC_ASCII_VALUE                 0x1b


dynamixel::PortHandler *portHandler;
dynamixel::PacketHandler *packetHandler;

// Communication result
int dxl_comm_result = COMM_TX_FAIL;
uint8_t dxl_error = 0;
uint16_t ax_present_position = 0;
uint16_t ax_previous_position = 0xffff;
uint16_t ax_moving_speed = 200;

bool position_output = false;
int revolution_count = 0;
bool value_between_500_510 = false;
bool value_between_513_523 = false;
uint32_t revolution_start_time;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Start..");

  portHandler = dynamixel::PortHandler::getPortHandler(DEVICENAME);
  // Initialize PacketHandler instance
  // Set the protocol version
  // Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
  packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);

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
  // Change Dynamixel CW Angle Limit
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
  // Enable Dynamixel Torque
  dxl_comm_result = packetHandler->write1ByteTxRx(portHandler, DXL_ID, AX_TORQUE_ENABLE, TORQUE_ENABLE, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS)
  {
    packetHandler->getTxRxResult(dxl_comm_result);
  }
  else if (dxl_error != 0)
  {
    //packetHandler->printRxPacketError(dxl_error);
  }
  else
  {
    Serial.print("Dynamixel has been successfully connected!\n");
  }

  // Write out startup speed
  dxl_comm_result = packetHandler->write2ByteTxRx(portHandler, DXL_ID, AX_GOAL_SPEED_L, ax_moving_speed , &dxl_error);
  PrintErrorStatus("AX_GOAL_SPEED_L", dxl_comm_result, dxl_error);
  revolution_start_time = millis();
}


void loop() {

  // Read present Position
  //dxl_comm_result = packetHandler->read2ByteTxRx(portHandler, DXL_ID, AX_PRESENT_POSITION_L, &ax_present_position , &dxl_error);
  //PrintErrorStatus("AX_PRESENT_POSITION_L", dxl_comm_result, dxl_error);
  if (ax_present_position != ax_previous_position) {

    if (position_output) {
      Serial.printf("[ID:%03d] Pres:%d\n", DXL_ID, ax_present_position);
    }

    // Lets try looking around the half way mark of 512 as around 1024-0 transsition there is 60 degrees of
    // not any valid values...
    // 
    if      ((ax_present_position >= 500) && (ax_present_position <= 510)) value_between_500_510 = true;
    else if ((ax_present_position >= 513) && (ax_present_position <= 523)) value_between_513_523 = true;
    else if ((ax_present_position <  500) || (ax_present_position >  523)) {
      value_between_500_510 = false;
      value_between_513_523 = false;
    }
    // if both values are set
    if (value_between_500_510 && value_between_513_523) {
      if (ax_moving_speed < 1024) revolution_count++;
      else revolution_count--;
      Serial.printf("Revl: %d Dt:%u\n", revolution_count, millis()-revolution_start_time);
      revolution_start_time = millis();
      value_between_500_510 = false;
      value_between_513_523 = false;
    }
    ax_previous_position = ax_present_position;
  }


  if (Serial.available()) {
    uint16_t new_goal_speed = 0;
    int ch;
    while (Serial.available()) {
      ch = Serial.read();
      if ((ch >= '0') && (ch <= '9')) {
        new_goal_speed = new_goal_speed * 10 + ch - '0';
      } else if ((ch == 'p') || (ch == 'P')) {
        position_output = !position_output;
      }
    }
    if (new_goal_speed != ax_moving_speed) {
      // Write goal speed
      ax_moving_speed = new_goal_speed;
      dxl_comm_result = packetHandler->write2ByteTxRx(portHandler, DXL_ID, AX_GOAL_SPEED_L, ax_moving_speed , &dxl_error);
      PrintErrorStatus("AX_GOAL_SPEED_L", dxl_comm_result, dxl_error);

      if (ax_moving_speed < 1024) Serial.printf("New speed %d CCW\n", ax_moving_speed);
      else Serial.printf("New speed %d CW\n", ax_moving_speed-1024);
    }
  }
}

void PrintErrorStatus(const char *psz, int dxl_comm_result, uint8_t dxl_error)
{
  if (dxl_comm_result != COMM_SUCCESS)
  {
    Serial.print(psz);
    Serial.print(" ");
    Serial.println(packetHandler->getTxRxResult(dxl_comm_result));
  }
  else if (dxl_error != 0)
  {
    Serial.print(psz);
    Serial.print(" ");
    Serial.println(packetHandler->getRxPacketError(dxl_error));
  }
}
