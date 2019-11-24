# DXL_AX_12A


- This Repo has been created for Skill's Module for Bartlett AD, UCL. It contains Dynamixel SDK from https://github.com/ROBOTIS-GIT/DynamixelSDK. 
- Scripts are modified for robotis ax-12a servos.
- It contains control pipeline from Unity to pi, controlling dynamixel servos via udp protocol. 



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
- Please check Robotis e-manual for servo data sheet
 http://emanual.robotis.com/docs/en/dxl/ax/ax-12a/
- You may go through free python tutorials from Code Academy https://www.codecademy.com

## Linux Terminal Basic Commands
- run commands with administrative privileges(run as admin in Windows)
```bash
sudo
```
- used for installing or upgrading packages
```bash
apt-get
#or
sudo apt-get install
sudo apt-get upgrade
```
- List all files in the current folder
```bash
ls
```
- Change directory
```bash
cd /  # to root directory
cd -  # to previous directory
cd .. # to one up directory
```
- print working directory
```bash
pwd
```
- copy 
```bash
cp
#(eg. cp exampleCode.py /home/workshop would copy the file “exampleCode.py” to the directory “/home/workshop”)
```
- move 
```bash
mv
#(eg. mv exampleCode.py /home/workshop would move the file “exampleCode.py” to the directory “/home/workshop”)
```
- remove 
```bash
rmdir # removes an empty directory 
rm -r # removes a directory recursively
#(eg. mv exampleCode.py /home/workshop would move the file “exampleCode.py” to the directory “/home/workshop”)
```
- make directory 
```bash
mkdir
```
- edit script on pi
```bash
nano filename
#(eg. nano exampleCode.py)
```
- to logout from pi
```bash
logout
```
- to see usb connected 
```bash
lsusb
```
- to see connected device port address 
```bash
ls /dev/tty*
```

## In case U2D2 is not recognized 
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


