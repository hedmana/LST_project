import serial
import time

# Define the serial port and baud rate
ser = serial.Serial('COM12', 9600)  # Replace 'COM3' with your serial port

# Wait for the serial connection to establish
time.sleep(2)

while True:
    # Read the serial data
    serial_data = ser.readline().decode('utf-8').strip()

    # Convert the serial data to integer
    sensor_value = int(serial_data)

    # Print the received sensor value
    print("Received sensor value:", sensor_value)

    # Add your processing logic here

    # Wait for a moment before reading again
    time.sleep(0.5)
