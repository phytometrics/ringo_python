# 使用例

RINGOパッケージの使用例を紹介します。

## 基本的な使用例

### コンテキストマネージャを使用した例

```python
from ringo import SerialSensorWrapper
import time

# シリアルポートに接続
port = "/dev/ttyUSB0"  # Windowsの場合は "COM3" など
baudrate = 115200

# コンテキストマネージャを使用（自動的に接続・切断を行います）
with SerialSensorWrapper(port, baudrate=baudrate) as sensor:
    if sensor.is_connected():
        # データを送信
        sensor.write_data("COMMAND\r\n")
        
        # 応答を待つ
        time.sleep(0.5)
        
        # データを受信
        data = sensor.read_line()
        if data:
            print(f"受信データ: {data.decode('utf-8', errors='ignore').strip()}")
    else:
        print("接続できませんでした")
```

### 手動での接続・切断

```python
from ringo import SerialSensorWrapper
import time

# インスタンスを作成
sensor = SerialSensorWrapper("/dev/ttyUSB0", baudrate=115200)

try:
    # 接続
    sensor.open()

    if sensor.is_connected():
        # データを送信
        sensor.write_data("COMMAND\r\n")
        
        # 応答を待つ
        time.sleep(0.5)
        
        # データを受信
        data = sensor.read_line()
        if data:
            print(f"受信データ: {data.decode('utf-8', errors='ignore').strip()}")
    else:
        print("接続できませんでした")
finally:
    # 切断
    sensor.close()
```

## 応用例

### 継続的なデータ読み取り

```python
from ringo import SerialSensorWrapper
import time

with SerialSensorWrapper("/dev/ttyUSB0", baudrate=115200) as sensor:
    if sensor.is_connected():
        # 10回データを読み取る
        for i in range(10):
            data = sensor.read_line()
            if data:
                print(f"データ {i+1}: {data.decode('utf-8', errors='ignore').strip()}")
            time.sleep(1)
    else:
        print("接続できませんでした")
```

### 再接続機能の使用

```python
from ringo import SerialSensorWrapper
import time

sensor = SerialSensorWrapper("/dev/ttyUSB0", baudrate=115200)
sensor.open()

try:
    for i in range(20):
        if sensor.is_connected():
            data = sensor.read_line()
            if data:
                print(f"データ: {data.decode('utf-8', errors='ignore').strip()}")
        else:
            print("接続が切れました。再接続を試みます...")
            sensor.reconnect()
            
        time.sleep(1)
finally:
    sensor.close()
```

### カスタムシリアルパラメータの使用

```python
from ringo import SerialSensorWrapper

# 追加のシリアルパラメータを指定
sensor = SerialSensorWrapper(
    port="/dev/ttyUSB0",
    baudrate=9600,
    timeout=2,
    bytesize=8,
    parity='N',
    stopbits=1,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False
)

sensor.open()
if sensor.is_connected():
    print("接続成功")
    # ...
sensor.close()
```

### バイナリデータの送受信

```python
from ringo import SerialSensorWrapper
import time

with SerialSensorWrapper("/dev/ttyUSB0", baudrate=115200) as sensor:
    if sensor.is_connected():
        # バイナリデータを送信
        binary_data = bytes([0x01, 0x02, 0x03, 0x04])
        sensor.write_data(binary_data)
        
        # 応答を待つ
        time.sleep(0.5)
        
        # データを受信
        data = sensor.read_line()
        if data:
            # バイナリデータを16進数で表示
            hex_data = ' '.join(f'{b:02x}' for b in data)
            print(f"受信データ (HEX): {hex_data}")
    else:
        print("接続できませんでした")
```

### ロギングレベルの変更

```python
import logging
from ringo import SerialSensorWrapper

# ロギングレベルをDEBUGに変更（より詳細なログが出力されます）
logging.getLogger().setLevel(logging.DEBUG)

# ファイルにもログを出力
file_handler = logging.FileHandler('serial_communication.log')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(file_handler)

# 通常通り使用
with SerialSensorWrapper("/dev/ttyUSB0", baudrate=115200) as sensor:
    if sensor.is_connected():
        sensor.write_data("TEST\r\n")
        data = sensor.read_line()
        if data:
            print(f"受信データ: {data.decode('utf-8', errors='ignore').strip()}")
```

## 実際のデバイスとの通信例

### Arduinoとの通信

```python
from ringo import SerialSensorWrapper
import time

# Arduinoが接続されているポートを指定
port = "/dev/ttyACM0"  # Windowsの場合は "COM3" など
baudrate = 9600  # Arduinoのスケッチで設定したボーレートと同じ値

with SerialSensorWrapper(port, baudrate=baudrate) as arduino:
    if arduino.is_connected():
        print("Arduinoに接続しました")
        
        # LEDをオンにするコマンドを送信
        arduino.write_data("LED_ON\n")
        time.sleep(1)
        
        # LEDをオフにするコマンドを送信
        arduino.write_data("LED_OFF\n")
        time.sleep(1)
        
        # センサーデータを要求
        arduino.write_data("GET_SENSOR\n")
        
        # 応答を待つ
        time.sleep(0.5)
        
        # データを受信
        data = arduino.read_line()
        if data:
            print(f"センサーデータ: {data.decode('utf-8', errors='ignore').strip()}")
    else:
        print("Arduinoに接続できませんでした")
```

### GPSモジュールとの通信

```python
from ringo import SerialSensorWrapper
import time
import re

# GPSモジュールが接続されているポートを指定
port = "/dev/ttyUSB0"
baudrate = 9600

with SerialSensorWrapper(port, baudrate=baudrate) as gps:
    if gps.is_connected():
        print("GPSモジュールに接続しました")
        
        # NMEAセンテンスを10回読み取る
        for _ in range(10):
            data = gps.read_line()
            if data:
                nmea = data.decode('ascii', errors='ignore').strip()
                print(f"NMEA: {nmea}")
                
                # GGA（Global Positioning System Fix Data）センテンスを解析
                if nmea.startswith('$GPGGA'):
                    parts = nmea.split(',')
                    if len(parts) >= 6 and parts[2] and parts[4]:
                        lat = float(parts[2][:2]) + float(parts[2][2:]) / 60
                        if parts[3] == 'S':
                            lat = -lat
                            
                        lon = float(parts[4][:3]) + float(parts[4][3:]) / 60
                        if parts[5] == 'W':
                            lon = -lon
                            
                        print(f"緯度: {lat}, 経度: {lon}")
            
            time.sleep(1)
    else:
        print("GPSモジュールに接続できませんでした")
