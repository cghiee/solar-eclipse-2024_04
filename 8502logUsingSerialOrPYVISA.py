import serial
import time
import pyvisa

# The device file for the USB to TTL adapter
serial_port = '/dev/tty.usbserial-14330'
baud_rate = 9600  # Adjust as needed to match your device's requirements

# Open the serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Ensure the serial port is open
if ser.is_open:
    print(f"Serial port {serial_port} is open.")
else:
    print(f"Failed to open serial port {serial_port}.")

# Loop for 1 minute, taking a reading every second
for i in range(10):
    # Sending a command to request current measurement
    # Replace 'MEAS:CURR?' with the actual command for your device
    command = "MEAS:CURR?\r\n"
    ser.write(command.encode())
    
    # Reading the response
    response = ser.readline().decode().strip()
    print(f"Current reading {i+1}: {response}")
    
    # Wait for 1 second before the next reading
    time.sleep(1)

# Close the serial port
ser.close()

print(" I GOT SERIAL ******************")
# Configuration for your specific instrument
serial_port = '/dev/tty.usbserial-14330'  # Update with the correct port
baud_rate = 9600  # Adjust according to your instrument's settings
timeout = 2  # Increase if necessary to allow for instrument response

try:
    with serial.Serial(serial_port, baud_rate, timeout=timeout) as ser:
        time.sleep(1)  # Wait for connection stabilization

        # Clear any data from the buffer
        ser.reset_input_buffer()
        
        # Send the SCPI command to request the instrument's identification
        ser.write(b'*IDN?\r\n')
        time.sleep(1)  # Wait for the instrument to process the command

        # Read and print the response
        response = ser.readline().decode().strip()
        print(f"Response: {response}")
except Exception as e:
    print(f"Error communicating with the instrument: {e}")

# Initialize the ResourceManager with the PyVISA-py backend explicitly
rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())
print("RESOURCE LIST DONE------------------------")

# Use the same ResourceManager instance to open the serial resource
instrument = rm.open_resource('ASRL/dev/cu.usbserial-14330::INSTR', timeout=5000)
#instrument = rm.open_resource('ASRL1::INSTR', timeout=5000)
#instrument = rm.open_resource('/dev/cu.usbserial-14330', timeout=5000)

print("INSTRUMENT CONNECTED")
print(instrument.query('*IDN?'))
print("QUERY DONE using pyvisa in SCPI to cu.usbserial--")
