import serial
from datetime import datetime

# Configure the serial port
ser = serial.Serial(
    port='/dev/ttyACM0',        # Replace with your port name
    baudrate=9600,              # Baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1                   # Read timeout in seconds
)

# Function to parse the received data
def parse_data(data):
    data_dict = {}
    try:
        if "R:" in data and "G:" in data and "B:" in data:
            parts = data.split()
            data_dict['R'] = int(parts[1])
            data_dict['G'] = int(parts[3])
            data_dict['B'] = int(parts[5])
        elif "Temperature" in data:
            data_dict['temperature'] = float(data.split('=')[1].split('*')[0].strip())
        elif "Pressure" in data:
            data_dict['pressure'] = float(data.split('=')[1].split('hPa')[0].strip())
        elif "Approx. Altitude" in data:
            data_dict['approx_altitude'] = float(data.split('=')[1].split('m')[0].strip())
        elif "Humidity" in data:
            data_dict['humidity'] = float(data.split('=')[1].split('%')[0].strip())
    except (IndexError, ValueError) as e:
        print(f"Error parsing data: {data} -> {e}")
    return data_dict

# Function to check if all required data is present
def all_data_received(data_dict):
    required_keys = {'R', 'G', 'B', 'temperature', 'pressure', 'approx_altitude', 'humidity'}
    return required_keys.issubset(data_dict.keys())

# Dictionary to hold all data
all_data = {}

try:
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8').rstrip()
            parsed_data = parse_data(raw_data)
            if parsed_data:
                all_data.update(parsed_data)
                if all_data_received(all_data):
                    timestamp = datetime.now().isoformat()
                    combined_data = {'timestamp': timestamp}
                    combined_data.update(all_data)
                    print(combined_data)
                    all_data = {}  # Clear the dictionary for the next set of data
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    ser.close()
    print("Serial port closed")
