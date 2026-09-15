# Prologix GPIB-USB Controller KISS Driver for Python 3
A 'Keep It Simple Stupid' (KISS) Python Driver for the Prologix GPIB-USB Controller.  

There are other drivers available. One encapsulates the instruments functionality, another adds AsyncIO threading. Both are nice.  

However, there is a need for a bare minimum, 'Keep It Simple Stupid' or KISS driver that doesn't take an hour to get going.
  
Why? Because many times I have a need to quickly throw together a few GPIB instruments to make a one off measurement that requires only a few commands to be sent to a few instruments. No need to spend time 'encapsulating' the instruments functionality into a full blown class and no need for AsyncIO.  
  
This driver fulfills this need. Bare minimum GPIB functionality that can get you talking to an instrument very quickly.  
  
If you know the basic SCPI commands that you need to configure your instrument, and make a measurement, then that is all you need. No spending hours writing more code or figuring out a more complicated driver.  

### Driver KISS Philosophy:
This driver is based on the 'old' HP Basic model of ```OUTPUT``` and ```ENTER``` commands like,
``` 
ASSIGN @Dmm TO 722      ! 22 is the Instrument Address
OUTPUT @Dmm; "*IDN?"    ! Send the command
ENTER @Dmm; Rdg         ! Get the result
PRINT Rdg               ! print the result
```
Where each write (OUTPUT) or read (ENTER) includes the instruments GPIB address and the command string. Simple to understand and fast to get going.  
  
This driver is just as simple as the only instrument commands are ```write(inst_address, cmd_str)``` and ```write_read(inst_address, cmd_str)```. The driver takes care of adding and removing the string terminator characters appropriately, and also takes care of properly setting the GPIB address in the Prologix controller.  

The equivalent code to above using this driver with Python is,
``` Python
import prologix_usb_to_gpib            # Import the driver
gpib = PrologixUsbToGpib(com_port=10)  # Setup with the COM port of the Prologix adapter, get a handle
rdg = gpib.write_read(22, '*IDN?')     # Send command to instrument at address 22, get response.
print(rdg)                             # Print the result
```
  
### Usage:
1) Get the code from the 'src' directory here, and place it somewhere where your Python program can find it.  
2) Use this simple outline to get going,  
   ``` Python  
    inst_addr = 22                          # 22 is the instrument GPIB address
    gpib = PrologixGpibUsb(com_port=10)     # 10 is the COM port that the Prologix adapter is on

    # ----- These next properties are optional, defaults normally work just fine -----

    # I have to use this on very old instruments, sometimes as long as 1 second.
    # None of my 'modern' SCPI enabled instruments require this.
    # This is the delay from when an write ends, to when a read begins.
    # None (or 0) sets 0 delay. Default is None
    gpib.write_to_read_delay_sec = None

    # On long operations sometimes a very long read timeout is required.
    # Default is 10 seconds to follow default for most GPIB cards.
    # None is blocking until the termination characters are received,
    # 0 is non-blocking returns immediately with any data.
    gpib.read_timeout_sec = 10

    # Some older instruments are 'funny' as to the terminator,
    # this shows how to set a line terminator if you need to.
    # Default is '\r\n'
    gpib.terminator = '\r\n'
    # ----------------------------------------------------------------------

    # Simple write a command with no response
    gpib.write(inst_addr, '*CLS')

    # Simple compound command write, wait for complete response
    opc = gpib.write_read(inst_addr, '*RST;*OPC?')
    print(f'{opc = }')
   
    # Get the *IDN? String
    idn = gpib.write_read(inst_addr, '*IDN?')
    print(f'{idn = }')

    # Get any errors
    err = gpib.write_read(inst_addr, 'SYSTem:ERRor?')
    print(f'{err = }')

    sys.exit()

    """
    For a HP34401 DVM at address 22, this will print,

        opc = '1'
        idn = 'HEWLETT-PACKARD,34401A,0,11-5-2'
        err = '+0,"No error"'

    If the instrument can't be found the '*IDN?' will return '', meaning a timeout.

    Note: Not all GPIB instruments support the simple commands tested above.
    Most support '*IDN?' however.
    """
   ```
     
#### User Hint: 
I always 'fix' the COM Port of my Prologix Adapter to a specific COM port so I don't have to remember what port the PC assigned to the Adapter. Then I write this COM Port number on my adapter for easy 'recall'. On Windows, a specific COM port can be set by going to: 'Device Manager', then selecting the Prologix COM port that Windows assigned, right click and select 'Driver', then go to 'Advanced' and set a fixed COM port (one that isn't already in use by the PC). I usually pick COM port 10, but you can pick anything that isn't already in use by the PC. Now your code will work on any PC that you have 'set' and and you don't have to worry about the PC changing the port on you in the future, breaking your code.
  
### User Settable Properties:  
The default properties will work for the majority of modern SCPI instruments. However for older instruments some of these properties may need to be changed. All these properties can be set on the fly and the next commands(s) will use them.  
  
### Driver Class Outline 'Tree View':  
```
prologix_gpib_usb.py
└── PrologixGpibUsb
    ├── __init__()
    ├── __del__()
    ├── _to_bytes()
    ├── _to_string()
    ├── _check_address()
    ├── read_timeout_sec() @property
    ├── read_timeout_sec() @read_timeout_sec.setter
    ├── write_timeout_sec() @property
    ├── write_timeout_sec() @write_timeout_sec.setter
    ├── write_to_read_delay_sec() @property
    ├── write_to_read_delay_sec() @write_to_read_delay_sec.setter
    ├── terminator() @property
    ├── terminator() @terminator.setter
    ├── write()
    └── write_read()
```
    
### Testing:  
Tested on: Windows 7, 10 & 11 with Python 3.12. Since the heart of the code is based on PySerial and PySerial is cross platform, this driver should work on any OS that PySerial and the FTDI VCP driver supports.  

### References:
* Source for Prologix USb to GPIB Adapters: https://prologix.biz/  
  
