import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import count

# Set up the serial connection (adjust the port and baud rate according to your setup)
ser = serial.Serial('/dev/cu.usbserial-2140', 115200)  # Update to your serial 
try:
  ser2 = serial.Serial('/dev/cu.usbmodem21101', 115200)  # Update to your second serial port
except Exception:
    ser2 = None
    print("error")


# This generator function reads from the serial port
def read_latest_from_port(serial_connection):
    serial_connection.reset_input_buffer()  # Flush the input buffer to discard any old data
    reading = serial_connection.readline().decode('utf-8').strip()  # Then read the next available data
    return reading

# Initialize matplotlib for live plotting
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # Create a second y-axis

x_data, y1_data, y2_data = [], [], []
index = count()

# This function is called periodically by FuncAnimation
def animate(i):
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
    if y1 <= 0 or y2 <= 0:
        return
    
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

    

# Create an animation by repeatedly calling the animate function every 1000 ms
ani = animation.FuncAnimation(fig, animate, interval=100)

plt.show()

# Don't forget to close the serial port when you're done
ser.close()
if ser2:
    ser2.close()
