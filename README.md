# Prologix-GPIB-USB-Controller-KISS-Driver-for-Python
A 'Keep It Simple Stupid' (KISS) Python Driver for the Prologix GPIB-USB Controller.  

There are other drivers available. One encapsulates the instruments functionality, another adds AsyncIO threading. Both are nice.  

However, there is a need for a bare minimum, 'Keep It Simple Stupid' or KISS driver that doesn't take an hour to get going.
  
Why? Because many times I have a need to quickly throw together a few GPIB instrumets to make a one off measurement that requires only a few commands to be sent to a few instruments. No need to waste time 'encapsulating' the instruments functionality into a full blown class and no need for AsyncIO.  
  
This driver fulfills this need. Basic GPIB functionality that can get you talking to an instrument very quickly.  
  
Usage:

1) Get the code here, from the 'src' directory, and place it somewhere where your program can find it.  
2) Use this simple outline to get going,  
   ```  
   place code here
   ```  
  
That's all! If you know the basic SCPI commands that you need to make a measurement, then that is all you need.  
  
Tested on: Windows 7, 10 & 11 with Python 3.12. Since the heart of the code is based on PySerial and PySerial is cross platform, this driver should work on any OS that PySerial supports.  
  
