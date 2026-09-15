# Prologix-GPIB-USB-Controller-KISS-Driver-for-Python
A 'Keep It Simple Stupid' (KISS) Python Driver for the Prologix GPIB-USB Controller.  

There are other drivers available. One encapsulates the instruments functionality, another adds AsyncIO threading. Both are nice.  

However, there is a need for a bare minimum, 'Keep It Simple Stupid' or KISS driver that doesn't take an hour to get going.
  
Why? Because many times I have a need to quickly throw together a few GPIB instrumets to make a one off measurement that requires only a few commands to be sent to a few instruments. No need to waste time 'encapsulating' the instruments functionality into a full blown class and no need for AsyncIO.  
  
This driver fulfills this need. Basic GPIB functionality that can get you talking to an instrument very quickly.  
  
That's all! If you know the basic SCPI commands that you need to configure your instrument, and make a measurement, then that is all you need. No spending hours writing more code.  

### Driver KISS Philosophy:
This driver is based on the 'old' HP Basic model of ```OUTPUT``` and ```ENTER``` commands like,
```
ASSIGN @Dmm TO 722      ! 22 is the Instrument Address
OUTPUT @Dmm; "*IDN?"    ! Send the command
ENTER @Dmm; Rdg         ! Get the result
PRINT Rdg               ! print the result
```
Where each write or read includes the instruments GPIB address and the command string. Simple to understand and fast to get going.  
  
This driver is just as simple as the only instrument commands are ```write(inst_address, cmd_str)``` and ```write_read(inst_address, cmd_str)```. The driver takes care of adding and removing the string terminator characters appropriately, and also takes care of properly setting the GPIB address in the Prologix controller.  

The equivalent code using this driver in Python is,
```
import prologix_usb_to_gpib            # Import the driver
gpib = PrologixUsbToGpib(com_port=10)  # Setup with the COM port of the Prologix adapter, get a handle
rdg = gpib.write_read(22, '*IDN?")     # Send command, get response.
print(rdg)                             # Print the result
```
  
### Usage:
1) Get the code here, from the 'src' directory, and place it somewhere where your program can find it.  
2) Use this simple outline to get going,  
   ```  
   place code here
   ```  
  
Tested on: Windows 7, 10 & 11 with Python 3.12. Since the heart of the code is based on PySerial and PySerial is cross platform, this driver should work on any OS that PySerial supports.  
  
