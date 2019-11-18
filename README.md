# DXL_AX_12A

control pipeline from Unity to pi, controlling dynamixel servos via udp protocol


## Prerequisite

- python 3
- dynamixel sdk
- python-osc (python 3)
- unity3d
- pip3


## Material

- Raspberry pi 
- Robotis Dynamixel AX_12A
- U2D2
- SMPS2Dynamixel
- 12V DC Adaptor
- Micro USB cable
- Micro USB (female) cable (if using pi zero)

## Unity
![](unity_servoControl_interface.png)
- type address pattern and servoid + "#" + value (eg. "writeGoalPos" and "1#720")


## Additional Resources

- Google drive link for wpa_config and linux(desbian)-also available from rasbian website
 https://drive.google.com/open?id=1oLfMgb-lJGOaOLKiIynS6E6ps8A851XD

## In U2D2 is not recognized 
- download Dynamixel Wizard to double check the id and baudrate of servo
- check the port name from device manager(in Windows)
- if not visible in the device manager download ftdi driver
- In Linux 
```bash
ls /dev/tty* # generally its /dev/ttyUSB0
# or
lsusb # to check how many driver is plugged
```
## In case your laptop can not recieve udp message
- check the Firewall settings in Windows and make a new inbound rule


