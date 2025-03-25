import serial
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SerialSensorWrapper:
    def __init__(self, port, baudrate=9600, timeout=1, **kwargs):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_args = kwargs
        self.ser = None

    def open(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                **self.serial_args
            )
            time.sleep(2)  # 通信初期化のため少し待つ
            logging.info(f"Connected to {self.port} at {self.baudrate} baud")
        except serial.SerialException as e:
            logging.error(f"Failed to open serial port: {e}")
            self.ser = None

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            logging.info("Serial connection closed")

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def read_line(self):
        if self.is_connected():
            try:
                data = self.ser.readline()
                return data
            except serial.SerialException as e:
                logging.error(f"Read error: {e}")
        else:
            logging.warning("Read attempted on closed connection")
        return None

    def write_data(self, data):
        if self.is_connected():
            try:
                if isinstance(data, str):
                    data = data.encode('utf-8')
                self.ser.write(data)
                logging.debug(f"Sent: {data}")
            except serial.SerialException as e:
                logging.error(f"Write error: {e}")
        else:
            logging.warning("Write attempted on closed connection")

    def reconnect(self):
        self.close()
        time.sleep(1)
        self.open()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

# if __name__ == "__main__":
#     port = "/dev/ttyUSB0"  # or COM3 on Windows

#     with SerialSensorWrapper(port, baudrate=115200) as sensor:
#         if sensor.is_connected():
#             for _ in range(10):
#                 line = sensor.read_line()
#                 if line:
#                     print(f"Received: {line.decode('utf-8', errors='ignore').strip()}")
#                 time.sleep(1)
#         else:
#             logging.error("Could not establish connection")
