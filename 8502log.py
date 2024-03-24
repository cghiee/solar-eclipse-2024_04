import serial
import time
import csv
from datetime import datetime
import os

def get_unique_filename(base_filename):
    """
    Generates a unique filename by adding a serial number if the base filename already exists.
    :param base_filename: The base name of the file, assumed to include the .csv extension
    :return: A unique filename based on the base filename
    """
    counter = 1
    filename_parts = base_filename.split('.')
    base = '.'.join(filename_parts[:-1])
    extension = filename_parts[-1]
    new_filename = base_filename

    # Check if the file exists and generate a new filename if necessary
    while os.path.exists(new_filename):
        new_filename = f"{base}_{counter}.{extension}"
        counter += 1
    
    return new_filename

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

# Base CSV file path
base_csv_file_path = 'current_measurements.csv'
# Get a unique filename
csv_file_path = get_unique_filename(base_csv_file_path)

# Open the CSV file for writing
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['UTC Timestamp', 'Current Measurement'])

    # Loop for 1 minute, taking a reading every second
    for i in range(60):
        # Sending a command to request current measurement
        # Replace 'MEAS:CURR?' with the actual command for your device
        command = "MEAS:CURR?\r\n"
        ser.write(command.encode())
        
        # Reading the response
        response = ser.readline().decode().strip()
        
        # Get the current UTC time
        utc_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"{utc_now}, Current reading {i+1}: {response}")
        
        # Write the timestamp and current reading to the CSV file
        writer.writerow([utc_now, response])
        
        # Wait for 1 second before the next reading
        time.sleep(1)

# Close the serial port
ser.close()

print(f"Data logging complete. Data saved to {csv_file_path}.")
