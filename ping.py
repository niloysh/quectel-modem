import serial
import time
import sys

# Configuration
PORT = "/dev/ttyUSB2"
BAUDRATE = 115200
PING_TARGET = "8.8.8.8"
INTERVAL = 5


def main():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=3)
        print(f"✔ Connected to {PORT} at {BAUDRATE} baud")

        while True:
            cmd = f'AT+QPING=1,"{PING_TARGET}",1,64'
            print(f"\nSending: {cmd}")
            ser.reset_input_buffer()
            ser.write((cmd + "\r").encode())

            # Wait for response
            time.sleep(2)
            response = ser.read_all().decode(errors="ignore").strip()
            print("Response:")
            print(response)

            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n✖ Interrupted by user.")
    except Exception as e:
        print(f"✖ Error: {e}")
    finally:
        try:
            ser.close()
            print("✔ Serial connection closed.")
        except:
            pass


if __name__ == "__main__":
    main()
