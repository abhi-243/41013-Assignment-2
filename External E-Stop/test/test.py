import serial
import time

# Replace COM3 with the Teensy COM port on your PC
ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)  # wait for Teensy to initialize

print("Listening for button presses... (Ctrl+C to exit)")

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(line)
except KeyboardInterrupt:
    print("\nExiting...")
    ser.close()