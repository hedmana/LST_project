import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import count
import pandas as pd
from datetime import datetime
import os


def initialize_serial():
    # Set up the serial connection (adjust the port and baud rate according to your setup)
    ser = serial.Serial('/dev/cu.usbserial-2140', 115200)  # Update to your serial
    try:
        ser2 = serial.Serial('/dev/cu.usbmodem21101', 115200)  # Update to your second serial port
    except Exception:
        ser2 = None
        print("error")

    return ser, ser2


# This generator function reads from the serial port
def read_latest_from_port(serial_connection):
    serial_connection.reset_input_buffer()  # Flush the input buffer to discard any old data
    reading = serial_connection.readline().decode('utf-8').strip()  # Then read the next available data
    return reading


def results_to_excel(temp, res, output_filename):
    # Check if the file already exists
    if not os.path.exists(output_filename):
        # If the file doesn't exist, create a new dataframe with column names
        df = pd.DataFrame(columns=['time', 'temperature', 'resistance'])
    else:
        # If the file exists, load the existing dataframe
        df = pd.read_excel(output_filename)

    # Get current datetime
    current_time = datetime.now()

    # Create a new row with the current data
    new_row = {'time': current_time, 'temperature': temp, 'resistance': res}
    # Append the new row to the dataframe
    df = df.append(new_row, ignore_index=True)

    # Write the dataframe to the Excel file
    with pd.ExcelWriter(output_filename, mode='w', engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Results', index=False)
    writer.close()

# This function is called periodically by FuncAnimation
def animate(i,ser,ser2, index, x_data, y1_data, y2_data, ax1, ax2, output_filename):
    # Read data from the first serial port
    data1 = read_latest_from_port(ser)
    # Read data from the second serial port
    if (ser2):
      data2 = read_latest_from_port(ser2)
    else: 
        data2 = "0,0"
    
    try:
        parts2 = data2.split(',')
        y2 = float(parts2[0])  # First serial port data
    except ValueError as e:
        y2 = float(0) # First serial port data
        print(f"Failed to convert data2 to float: {data2}")

    try:
        parts1 = data1.split(',')
        y1 = float(parts1[0])  # First serial port data
    except ValueError as e:
        y1 = float(0) # First serial port data
        print(f"Failed to convert data1 to float: {data1}")

    # Skip non-positive values if using a log scale
    if y1 <= 10 or y2 <= 10:
        return

    results_to_excel(y1,y2, output_filename)

    print(y1, y2)

    x = next(index)
    x_data.append(x)
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
    output_filename = f"{time_str}.xlsx"
    return output_filename


def main():
    # open serial ports
    ser, ser2 = initialize_serial()

    #get outputfile name
    output_filename = get_output_filename()

    # Initialize matplotlib for live plotting
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # Create a second y-axis
    x_data, y1_data, y2_data = [], [], []
    index = count()

    # Create an animation by repeatedly calling the animate function every 1000 ms
    ani = animation.FuncAnimation(fig, animate, fargs= [ser, ser2, index, x_data, y1_data, y2_data, ax1, ax2, output_filename], interval=100)

    plt.show()

    # Don't forget to close the serial port when you're done
    ser.close()
    if ser2:
      ser2.close()

if __name__ == "__main__":
    main()
