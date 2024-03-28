

### SET SCPI as the protocol on the 8502B Electronic load.
import serial
import time
import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import signal
import sys

# Initialize a global variable to control the loop
global should_continue
should_continue = True

def signal_handler(sig, frame):
    """
    Handle external signals to gracefully terminate the program.
    """
    global should_continue
    print('Termination signal received, stopping...')
    should_continue = False
    # Close resources here if needed immediately
    # For example: ser.close()

# Attach the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)


# Your existing functions and setup code goes here

# The device file for the USB to TTL adapter
serial_port = '/dev/tty.usbserial-14320'
baud_rate = 9600  # Adjust as needed
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Ensure the serial port is open
if ser.is_open:
    print(f"Serial port {serial_port} is open.")
else:
    print(f"Failed to open serial port {serial_port}.")

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
base_csv_file_path = 'current_measurements.csv'
csv_file_path = get_unique_filename(base_csv_file_path)

x_data, y_data = [], []

fig, ax = plt.subplots()
ax.set_title('Real-Time Current Measurements')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Current (A)')

line, = ax.plot(x_data, y_data)

# Parameter for the number of hours to plot
hours_to_plot = 1  # Example: 1 hour
# Calculate the total number of iterations (1 hour = 3600 seconds)
total_iterations = hours_to_plot * 3600

# Modify the update function to stop after reaching the total number of iterations

    # Modify your update function to check the should_continue flag
def update(frame):
    global should_continue
    if not should_continue or len(x_data) >= total_iterations:
        ani.event_source.stop()
        ser.close()
        print(f"Data logging complete. Data saved to {csv_file_path}.")
        plt.close(fig)  # Close the plot window
        sys.exit(0)  # Ensure the script exits
        return line,
        
    if len(x_data) >= total_iterations:
        ani.event_source.stop()
        ser.close()
        print(f"Data logging complete. Data saved to {csv_file_path}.")
        plt.close(fig)  # Close the plot window
        return line,

    command = "MEAS:CURR?\r\n"
    ser.write(command.encode())
    response = ser.readline().decode().strip()

    utc_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{utc_now}, Current reading {len(x_data) + 1}: {response}")

    x_data.append(len(x_data) + 1)
    y_data.append(float(response))

    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([utc_now, response])

    return line,

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['UTC Timestamp', 'Current Measurement'])

ani = FuncAnimation(fig, update, interval=1000)

plt.show()