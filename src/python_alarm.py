import serial
from time import sleep
import math


def initialize_serial():
    # list devices
    # Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' }


    # Set up the serial connection (adjust the port and baud rate according to your setup)
    #ser_res = serial.Serial('/dev/cu.usbserial-2140', 115200)  # Update to your serial
    ser_res = serial.Serial('COM6', 115200) # ser_res is resistance
    #ser_res = None
    try:
        #ser_arduino = serial.Serial('/dev/cu.usbmodem21101', 115200)  # Update to your second serial port
        ser_arduino = serial.Serial('COM12', 115200) # ser_arduino is temperature
    except Exception:
        ser_arduino = None
        print("error")

    return ser_res, ser_arduino

def read_resistance(ser_res):
    try:
        ser_res.reset_input_buffer()  # Flush the input buffer to discard any old data
        resistance_string = ser_res.readline().decode('utf-8').strip()

        resistance = float(resistance_string.split(',')[0])

    except:
        resistance = float(0) # First serial port data
        print(f"Failed to convert data2 to float: {resistance_string}")

    return resistance

def read_sine(counter):
    # Define parameters for sine wave
    amplitude = 1  # Amplitude of the sine wave
    frequency = 0.03  # Frequency of the sine wave (adjust to simulate fluctuations)
    offset = 0  # Offset of the sine wave

    # Generate value from sine wave
    output = amplitude * math.sin(2 * math.pi * frequency * counter) + offset
    return output

def loop(ser_res, ser_temp, alarm_low, alarm_high):
    counter = 0  # Initialize counter for sine wave

    while True:
        #resistance = read_resistance(ser_res)
        resistance = read_sine(counter)
        print(resistance)

        if resistance < alarm_low or resistance > alarm_high:
            ser_temp.write('1\n'.encode('utf-8'))

        sleep(1)
        counter += 1

def main():
    alarm_low = -0.75
    alarm_high = 0.75

    ser_res, ser_temp = initialize_serial()
    loop(ser_res, ser_temp, alarm_low, alarm_high)

if __name__ == "__main__":
    main()