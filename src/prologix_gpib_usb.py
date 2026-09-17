"""
Prologix GPIB-USB Adapter 'Keep it Simple Stupid' (KISS) Python Driver.

Written By: Steve Hageman Feb 2024, Updated Sept 2026
License: The Unlicense  https://unlicense.org/
Source: https://github.com/Hagtronics/Prologix-GPIB-USB-Controller-KISS-Driver-for-Python

Dependencies,
    FTDI VCP OS Driver for the Prologix USB/GPIB Adapter.
    pySerial 3.5 for the serial port access to the FTDI driver.
"""
import contextlib
import sys
import time

import serial  # PySerial


class PrologixGpibUsb:

    __version__ = '0.2'

    def __init__(self, com_port: int) -> None:
        """
        Prologix USB GPIB Adapter 'KISS' driver.

        Args:
            com_port (int): COM port where Prologix device is located.

        """
        # The instrument is addressed in the write() and write_read() functions
        self._addr: int = -1

        # These are properties that can be set
        self._read_timeout_sec: float | None = 10
        self._write_timeout_sec: float | None = None
        self._write_to_read_delay_sec: float = 0
        self._terminator: str = '\r\n'

        try:
            # open serial port, 9600 baud, 8 data bits, no parity, 1 stop bit,
            # 1 second timeout, no software flow control, RTS/CTS flow control
            #self._ser = serial.Serial(f'COM{com_port}',9600,8,'N',1,1,0,1,1)
            self._ser = serial.Serial(f'COM{com_port}',9600,8,'N',1, timeout=1)

        except Exception as e:
            print(e)
            sys.exit()

        # Set default timeouts
        self._ser.timeout = self._read_timeout_sec
        self._ser.write_timeout = self._write_timeout_sec

        # The first write is usually garbage, try and discard one write first
        self._ser.write('++ver\r\n'.encode('utf-8'))
        self._ser.flushInput()

        # This read should be good - Look for Prologix Device ID
        self._ser.write('++ver\r\n'.encode('utf-8'))
        rstr = str(self._ser.readline())
        if 'Prologix' not in rstr:
            self._ser.close()
            print(f'Unable to locate the Prologix USB/GPIB interface on specified COM port: {com_port}.')
            sys.exit()

        # These settings work in 99.9% of cases for modern SCPI Instruments
        self._ser.write('++read_tmo_ms 3000\r\n'.encode('utf-8'))   # set default tmo timeout to 3 seconds (Maximum)
        self._ser.write('++mode 1\r\n'.encode('utf-8'))             # put Prologix in controller mode
        self._ser.write('++auto 0\r\n'.encode('utf-8'))             # turn off Prologix Read-After-Write mode
        self._ser.write('++eoi 0\r\n'.encode('utf-8'))              # disable EOI assertion
        self._ser.write('++eos 2\r\n'.encode('utf-8'))              # append LF to instrument commands
        self._ser.write('++eot_enable 0\r\n'.encode('utf-8'))       # do not append character when EOI detected
        self._ser.write('++eot_char 0\r\n'.encode('utf-8'))         # This is the default value, but as per above it is not used
        self._ser.flushInput()                                      # discard serial data in serial input buffer

    def __del__(self) -> None:
        """ Destructor """
        with contextlib.suppress(BaseException):
            self._ser.close()



    # ===== Private Helpers =================================================
    def _to_bytes(self, string_in: str) -> bytes:
        return string_in.encode('utf-8')

    def _to_string(self, bytes_in: bytes) -> str:
        return bytes_in.decode('ascii')

    def _check_address(self, address: int) -> None:
        if address < 1 or address > 30:
            msg = f'GPIB Address: {address} is outside the valid range of 1 to 30.'
            raise ValueError(msg)

        if address != self._addr:
            self._addr = address
            self._ser.write(self._to_bytes(f'++addr {self._addr}\r\n'))


    # ===== Public Properties ==============================================
    @property
    def read_timeout_sec(self):
        """
        read_timeout_sec (float): None is blocking, 0 is non-blocking returns immediately with any data,
        else the timeout in seconds.
        Default is: 10 Seconds
        """
        return self._read_timeout_sec

    @read_timeout_sec.setter
    def read_timeout_sec(self, value: float | None) -> None:
        self._read_timeout_sec = value
        self._ser.timeout = self._read_timeout_sec


    @property
    def write_timeout_sec(self):
        """
        write_timeout_sec (float): None or 0 is forever, else the timeout in seconds.
        Default is: None
        """
        return self._write_timeout_sec

    @write_timeout_sec.setter
    def write_timeout_sec(self, value: float | None) -> None:
        self._write_timeout_sec = value
        self._ser.write_timeout = self._write_timeout_sec


    @property
    def write_to_read_delay_sec(self):
        """
        write_to_read_delay_sec (float): None is the same a zero seconds delay,
        else the delay in seconds to delay from the write to read function.
        Default is: None
        """
        return self._write_to_read_delay_sec

    @write_to_read_delay_sec.setter
    def write_to_read_delay_sec(self, value: float | None) -> None:
        if value is None:
            value = 0
        self._write_to_read_delay_sec = value


    @property
    def terminator(self):
        r"""
        Sets the terminator character(s) that will be sent after every command string.
        Default is: '\r\n'
        """
        return self._terminator

    @terminator.setter
    def terminator(self, value: str) -> None:
        self._terminator = value


    # ===== Public Write and WriteRead Functions ===========================
    def write(self, address: int, command: str) -> None:
        """
        Write Command To Instrument at address.
        Does not block.

        Args:
            address (int): The Instruments GPIB Address.
            command (str): The command to send to the instrument.

        """
        self._check_address(address)                                       # Set address if needed
        self._ser.write(self._to_bytes(command + self._terminator))        # Write the data and continue


    def write_read(self, address: int, command: str)->str:
        """
        Write Command Then Read Response from the Instrument at address.
        Blocks until LF terminator is read in response or read timeout happens.

        Args:
            address (int): The Instruments GPIB Address.
            command (str): The command to send to the instrument.

        Returns:
            str: The string that the instrument responded with.

        """
        self._check_address(address)                                       # Set address if needed
        self._ser.write(self._to_bytes(command + self._terminator))
        self._ser.flush()                                                  # Block until all bytes sent
        time.sleep(self._write_to_read_delay_sec)                          # Delay for slow instruments
        self._ser.write(self._to_bytes('++read 10' + self._terminator))    # Read until LF(10 dec) or timeout
        rval = self._to_string(self._ser.readline())
        return rval.rstrip('\r\n')                                         # Strip terminator(s)


# ===== Built in test code =================================================
if __name__ in '__main__':

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

    # Simple compound command write, get response
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

    If the instrument can't be found the '*OPC?' will return '',
    likely meaning a timeout.

    Note: Not all GPIB instruments support the simple commands
    tested above. Most support '*IDN?' however.
    """

