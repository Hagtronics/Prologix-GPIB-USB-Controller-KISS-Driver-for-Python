""" 
Simple example of a HP34401 reading a HP E3631A Power Supply.
As with most all modern SCPI instruments the driver here
runs just fine with all the default timeouts.

Program output is a table something like this,

    Set Voltage = 0.000    Error Voltage = 0.005
    Set Voltage = 0.100    Error Voltage = 0.003
    Set Voltage = 0.200    Error Voltage = 0.004
    ... ...
    Set Voltage = 5.800    Error Voltage = 0.009
    Set Voltage = 5.900    Error Voltage = 0.009
    Set Voltage = 6.000    Error Voltage = 0.010
    Fini...

License: The Unlicense, https://unlicense.org/
Source: https://github.com/Hagtronics/Prologix-GPIB-USB-Controller-KISS-Driver-for-Python
"""

# The prologix_gpib_usb.py file must be in the same directory
# as this script. Otherwise adjust the import accordingly.
import prologix_gpib_usb


# ===== Setup Prologix Adapter =====
# Set the COM port accordingly for your situation
gpib = prologix_gpib_usb.PrologixGpibUsb(com_port=10)


# ===== E3631 Setup =====
ADDR_PS = 5

# Reset PS, wait for *OPC? to return
_ = gpib.write_read(ADDR_PS, '*RST;*CLS;*OPC?')

# Turn the PS output on
gpib.write(ADDR_PS, 'OUTP ON')


# ===== HP34401 Setup =====
ADDR_DVM = 22
# Reset DVM, wait for *OPC? to return
_ = gpib.write_read(ADDR_DVM, '*RST;*CLS;*OPC?')


# ===== Big Loop =====
current_v = 0
step_v = 0.1
steps = 61

for _ in range(steps):
    
    # Set 3631 Voltage, wait for *OPC? return
    cmd = f'APPL P6V,{current_v:.1f},0.1;*OPC?'
    _ = gpib.write_read(ADDR_PS, cmd)
    
    # Read 34401 Voltage, convert string value return to a float
    cmd = 'MEAS:VOLT:DC? 10,0.001'
    reading_v = float(gpib.write_read(ADDR_DVM, cmd))

    # Calculate error
    error_v = reading_v - current_v
    
    # Print result
    print(f'Set Voltage = {current_v:.3f}    Error Voltage = {error_v:.3f}')
    
    # Update 'current' set voltage
    current_v += step_v

print('Fini...')