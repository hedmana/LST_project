import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import count
import csv
from datetime import datetime
import os
from time import sleep


def initialize_serial():
    # list devices
    # Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' }


    try:
      # Set up the serial connection (adjust the port and baud rate according to your setup)
      #ser_res = serial.Serial('/dev/cu.usbserial-1110', 115200)  # Update to your serial
      ser_res = serial.Serial('COM8', 115200) # ser_res is resistance
    except Exception:
      ser_res = None
      print("error ser_res")
    try:
        #ser_temp = serial.Serial('/dev/cu.usbmodem11401', 115200)  # Update to your second serial port
        ser_temp = serial.Serial('COM9', 115200) # ser_temp is temperature
    except Exception:
        ser_temp = None
        print("error ser_teml")

    return ser_res, ser_temp


# This generator function reads from the serial port
def read_latest_from_port(serial_connection):
    serial_connection.reset_input_buffer()  # Flush the input buffer to discard any old data
    reading = serial_connection.readline().decode('utf-8').strip()  # Then read the next available data
    return reading


def results_to_excel(temp, res, output_filename):
    # Check if the file already exists
    file_exists = os.path.exists(output_filename)
    
    # Open the file in append mode if it exists or write mode if it does not
    with open(output_filename, mode='a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)
        
        # If the file doesn't exist, write the header
        if not file_exists:
            writer.writerow(['time', 'temperature', 'resistance'])
        
        # Get current datetime
        current_time = datetime.now()
        
        # Write the data row
        writer.writerow([current_time, temp, res])

# This function is called periodically by FuncAnimation
def animate(i, ser_res, ser_temp, output_filename, x_data, y1_data, y2_data, ax1, ax2):

    y1, y2 = just_read_the_serial(ser_res, ser_temp, output_filename)

    if i == 0 or (abs(y2 - y2_data[-1]) < 1 and abs(y1 - y1_data[-1]) < 1): 
      x_data.append(i)
      y1_data.append(y1)
      y2_data.append(y2)
      
      ax1.clear()
      ax2.clear()
      
      # Plotting on the primary y-axis
      ax1.plot(x_data, y1_data, 'g-')
      # Plotting on the secondary y-axis
      ax2.plot(x_data, y2_data, 'b-')
      
      # Optionally, set y-axis labels
      ax1.set_ylabel('Resistance', color='g')
      ax2.set_ylabel('Temp', color='b')

    

def get_output_filename():
    current_time = datetime.now()
    # Format current datetime as string
    time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    # Construct output file name with datetime
    output_filename = f"{time_str}.csv"
    return output_filename


def give_arduino_parameters(ser, mode, heat_cycle_range):
    print("Giving Arduino some parameters...")

    # Check if there is data available in the input buffer
    text = ""
    while text != "Select mode":
        # Read and print the available data
        text = ser.readline().decode('utf-8').strip()  # Read a line and decode it
        print("Arduino: " + text)


    # Send parameters to the Arduino
    #ser.write(b'1\n')  # For example, sending '2' to the Arduino
    ser.write(f'{mode}\n'.encode('utf-8'))

    # verify which mode was selected
    text = ser.readline().decode('utf-8').strip()  # Read a line and decode it
    print("Arduino: " + text)

    # pass the range
    ser.write(f'{heat_cycle_range[0]},{heat_cycle_range[1]}\n'.encode('utf-8'))

    text = ser.readline().decode('utf-8').strip()  # Read a line and decode it
    print("Arduino: " +text)
    text = ser.readline().decode('utf-8').strip()  # Read a line and decode it
    print(text)
    text = ser.readline().decode('utf-8').strip()  # Read a line and decode it
    print(text)
    print("Arduino initialization complete.")



def just_read_the_serial(ser_res, ser_temp, output_filename):
    data1 = read_latest_from_port(ser_res)
    #data1 = "0,0"
    # Read data from the second serial port
    if (ser_temp):
        data2 = read_latest_from_port(ser_temp)
    else:
        data2 = "0,0"

    try:
        parts2 = data2.split(',')
        y2 = float(parts2[0])  # First serial port data
    except ValueError as e:
        y2 = float(0)  # First serial port data
        print(f"Failed to convert data2 to float: {data2}")

    try:
        # resistance
        parts1 = data1.split(',')
        y1 = float(parts1[0])  # First serial port data
    except ValueError as e:
        y1 = float(0)  # First serial port data
        print(f"Failed to convert data1 to float: {data1}")

    results_to_excel(y2, y1, output_filename)

    print(y1, y2)
    return y1, y2





def main():
    # open serial ports
    ser_res, ser_temp = initialize_serial()

    # Available modes
    # 1. cycle between given range
    # 2. cycle between given range, but stop for 30s at each degree increment and decrement ("temperature stairs")
    # 3. constant temperature (uses the heat_cycle_range[0] value)
    mode = 2
    heat_cycle_range = (35,40)

    give_arduino_parameters(ser_temp, mode, heat_cycle_range) # empty the temperature serial port

    #get outputfile name
    output_filename = get_output_filename()

    # Initialize matplotlib for live plotting
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # Create a second y-axis
    x_data, y1_data, y2_data = [], [], []
    index = count()

   
    # Create an animation by repeatedly calling the animate function every 1000 ms

    ani = animation.FuncAnimation(fig, animate, fargs= [ser_res, ser_temp, output_filename, x_data, y1_data, y2_data, ax1, ax2], interval=10)
    plt.show()



    #sleep(10)

    # Don't forget to close the serial port when you're done
    # ser.close()
    # if ser2:
    #   ser2.close()

if __name__ == "__main__":
    main()
