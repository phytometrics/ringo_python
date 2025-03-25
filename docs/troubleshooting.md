# トラブルシューティングガイド

RINGOパッケージを使用する際によくある問題とその解決方法を紹介します。

## 接続の問題

### シリアルポートが見つからない

**症状**: `SerialSensorWrapper`を初期化して`open()`を呼び出すと、以下のようなエラーが発生します。

```
Failed to open serial port: [Errno 2] could not open port /dev/ttyUSB0: [Errno 2] No such file or directory: '/dev/ttyUSB0'
```

**解決策**:

1. シリアルデバイスが正しく接続されているか確認してください。
2. 正しいポート名を指定しているか確認してください。
   - Linuxでは、`ls /dev/tty*`コマンドを実行して利用可能なシリアルポートを確認できます。
   - Windowsでは、デバイスマネージャーでポート（COM & LPT）を確認してください。
3. USBシリアル変換アダプタを使用している場合は、ドライバが正しくインストールされているか確認してください。

### アクセス権限の問題

**症状**: Linuxで以下のようなエラーが発生します。

```
Failed to open serial port: [Errno 13] could not open port /dev/ttyUSB0: [Errno 13] Permission denied: '/dev/ttyUSB0'
```

**解決策**:

1. ユーザーをdialoutグループに追加します。

   ```bash
   sudo usermod -a -G dialout $USER
   ```

   コマンド実行後、一度ログアウトして再ログインしてください。

2. または、一時的な解決策として、sudoでスクリプトを実行します。

   ```bash
   sudo python your_script.py
   ```

### ボーレートやその他の設定が正しくない

**症状**: 接続はできるが、データが正しく送受信できない、または文字化けする。

**解決策**:

1. デバイスの仕様書を確認して、正しいボーレート、データビット、パリティ、ストップビットを設定してください。

   ```python
   sensor = SerialSensorWrapper(
       port="/dev/ttyUSB0",
       baudrate=9600,  # デバイスに合わせて変更
       bytesize=8,
       parity='N',
       stopbits=1
   )
   ```

2. ハードウェアフロー制御（RTS/CTS、DSR/DTR）が必要かどうかを確認してください。

   ```python
   sensor = SerialSensorWrapper(
       port="/dev/ttyUSB0",
       baudrate=9600,
       rtscts=True,  # RTS/CTSフロー制御を有効化
       dsrdtr=True   # DSR/DTRフロー制御を有効化
   )
   ```

## データ送受信の問題

### データが受信できない

**症状**: `read_line()`を呼び出しても、データが返ってこない（`None`が返される）。

**解決策**:

1. デバイスが実際にデータを送信しているか確認してください。
2. タイムアウト値を増やしてみてください。

   ```python
   sensor = SerialSensorWrapper(port="/dev/ttyUSB0", baudrate=9600, timeout=5)
   ```

3. 行終端文字が正しいか確認してください。`read_line()`は改行文字（`\n`）を待ちます。
4. デバイスが改行文字を送信しない場合は、`read_line()`の代わりに`pyserial`の他のメソッドを使用することを検討してください。

### データが文字化けする

**症状**: 受信したデータをデコードすると、文字化けが発生する。

**解決策**:

1. 正しいエンコーディングを使用してデコードしてください。

   ```python
   data = sensor.read_line()
   if data:
       # ASCII以外の文字が含まれる場合は、適切なエンコーディングを指定
       text = data.decode('shift-jis', errors='ignore')  # 日本語の場合
       # または
       text = data.decode('utf-8', errors='ignore')
   ```

2. バイナリデータの場合は、デコードせずにバイト列として処理してください。

   ```python
   data = sensor.read_line()
   if data:
       # バイト列として処理
       hex_data = ' '.join(f'{b:02x}' for b in data)
       print(f"HEX: {hex_data}")
   ```

### 送信したコマンドに応答がない

**症状**: コマンドを送信しても、デバイスから応答がない。

**解決策**:

1. コマンドの形式が正しいか確認してください。特に行終端文字（CR、LF、CR+LF）が正しいか確認してください。

   ```python
   # CR+LF (Windows形式)
   sensor.write_data("COMMAND\r\n")
   
   # LF (Unix形式)
   sensor.write_data("COMMAND\n")
   
   # CR
   sensor.write_data("COMMAND\r")
   ```

2. デバイスが応答を返すまでの時間を確保してください。

   ```python
   sensor.write_data("COMMAND\r\n")
   time.sleep(0.5)  # デバイスの応答を待つ
   data = sensor.read_line()
   ```

3. デバイスがビジー状態でないことを確認してください。一部のデバイスは、特定の状態でのみコマンドを受け付けます。

## その他の問題

### インポートエラー

**症状**: `ImportError: No module named 'ringo'`というエラーが発生する。

**解決策**:

1. パッケージが正しくインストールされているか確認してください。

   ```bash
   pip list | grep ringo
   ```

2. 正しいPython環境で実行しているか確認してください。仮想環境を使用している場合は、その環境が有効になっているか確認してください。

3. パッケージを再インストールしてみてください。

   ```bash
   pip uninstall ringo
   pip install ringo
   ```

### pyserialのインストールに関する問題

**症状**: `pip install ringo`を実行すると、pyserialのインストールに関するエラーが発生する。

**解決策**:

1. pipを最新バージョンに更新してください。

   ```bash
   pip install --upgrade pip
   ```

2. 必要に応じて、pyserialを手動でインストールしてから、ringoをインストールしてください。

   ```bash
   pip install pyserial
   pip install ringo
   ```

3. Windowsでは、管理者権限でコマンドプロンプトを実行してインストールを試みてください。

### その他のエラー

予期しないエラーが発生した場合は、以下の情報を含めて問題を報告してください：

1. 使用しているPythonのバージョン
2. 使用しているOSとバージョン
3. エラーメッセージの全文
4. 問題を再現するための最小限のコード例

## デバッグ方法

問題の原因を特定するために、ロギングレベルをDEBUGに設定すると、より詳細な情報が得られます：

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)

# ファイルにログを出力
file_handler = logging.FileHandler('ringo_debug.log')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(file_handler)

# 通常通り使用
with SerialSensorWrapper("/dev/ttyUSB0", baudrate=115200) as sensor:
    # ...
```

これにより、シリアル通信の詳細なログが記録され、問題の診断に役立ちます。
