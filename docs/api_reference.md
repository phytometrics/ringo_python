# APIリファレンス

RINGOパッケージのAPIリファレンスです。

## SerialSensorWrapper

`SerialSensorWrapper`クラスは、シリアル通信を簡単に扱うためのラッパークラスです。

### コンストラクタ

```python
SerialSensorWrapper(port, baudrate=9600, timeout=1, **kwargs)
```

#### パラメータ

- `port` (str): シリアルポートの名前（例：'/dev/ttyUSB0'、'COM3'）
- `baudrate` (int, optional): ボーレート。デフォルトは9600
- `timeout` (float, optional): 読み取りタイムアウト（秒）。デフォルトは1
- `**kwargs`: `serial.Serial`クラスに渡される追加のキーワード引数

### メソッド

#### open()

シリアルポートを開きます。

```python
sensor.open()
```

**戻り値**: なし

**例外**:

- `serial.SerialException`: シリアルポートを開くことができない場合

#### close()

シリアルポートを閉じます。

```python
sensor.close()
```

**戻り値**: なし

#### is_connected()

シリアルポートが接続されているかどうかを確認します。

```python
if sensor.is_connected():
    # 接続されている場合の処理
```

**戻り値**:

- `bool`: 接続されている場合はTrue、そうでない場合はFalse

#### read_line()

シリアルポートから1行読み取ります。

```python
data = sensor.read_line()
if data:
    decoded_data = data.decode('utf-8', errors='ignore').strip()
```

**戻り値**:

- `bytes` or `None`: 読み取ったデータ。エラーが発生した場合やポートが閉じている場合はNone

**例外**:

- `serial.SerialException`: 読み取り中にエラーが発生した場合（内部でキャッチされる）

#### write_data(data)

シリアルポートにデータを書き込みます。

```python
sensor.write_data("COMMAND\r\n")  # 文字列の場合は自動的にエンコードされる
# または
sensor.write_data(b"COMMAND\r\n")  # バイト列を直接渡すこともできる
```

**パラメータ**:

- `data` (str or bytes): 書き込むデータ。文字列の場合はUTF-8でエンコードされる

**戻り値**: なし

**例外**:

- `serial.SerialException`: 書き込み中にエラーが発生した場合（内部でキャッチされる）

#### reconnect()

シリアルポートを一度閉じてから再接続します。

```python
sensor.reconnect()
```

**戻り値**: なし

### コンテキストマネージャのサポート

`SerialSensorWrapper`クラスはコンテキストマネージャプロトコルをサポートしているため、`with`文で使用できます。

```python
with SerialSensorWrapper('/dev/ttyUSB0', baudrate=115200) as sensor:
    # ブロック内でセンサーを使用
    # ブロックを抜けると自動的にclose()が呼ばれる
```

### 属性

- `port` (str): シリアルポートの名前
- `baudrate` (int): ボーレート
- `timeout` (float): 読み取りタイムアウト（秒）
- `serial_args` (dict): その他のシリアルポートパラメータ
- `ser` (serial.Serial or None): 内部で使用されるシリアルオブジェクト

## ロギング

RINGOパッケージは、Pythonの標準ロギングモジュールを使用してログを記録します。デフォルトでは、INFOレベル以上のログが標準出力に表示されます。

ロギングレベルやハンドラを変更するには、以下のようにします：

```python
import logging

# ロギングレベルを変更
logging.getLogger().setLevel(logging.DEBUG)

# ファイルにログを出力
file_handler = logging.FileHandler('ringo.log')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(file_handler)
