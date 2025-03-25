# RINGO ドキュメント

RINGOは、Pythonでシリアル通信を簡単に扱うためのラッパーパッケージです。

## 目次

### 入門

- [インストールガイド](installation.md) - RINGOのインストール方法
- [使用例](examples.md) - 基本的な使用例と応用例

### リファレンス

- [APIリファレンス](api_reference.md) - クラスとメソッドの詳細な説明

### サポート

- [トラブルシューティング](troubleshooting.md) - よくある問題と解決方法

## 概要

RINGOは、Pythonの`pyserial`ライブラリを使用して、シリアル通信を簡単に行うためのラッパークラスを提供します。
エラー処理やログ記録、コンテキストマネージャのサポートなど、シリアル通信を扱う際の一般的な機能を備えています。

### 主な機能

- シリアルポートへの接続・切断
- データの送受信
- エラー処理とログ記録
- コンテキストマネージャのサポート（`with`文での使用）
- 再接続機能

### 基本的な使用例

```python
from ringo import SerialSensorWrapper

# シリアルポートに接続
port = "/dev/ttyUSB0"  # Windowsの場合は "COM3" など
baudrate = 115200

# コンテキストマネージャを使用した例（自動的に接続・切断を行います）
with SerialSensorWrapper(port, baudrate=baudrate) as sensor:
    if sensor.is_connected():
        # データを送信
        sensor.write_data("COMMAND\r\n")
        
        # データを受信
        data = sensor.read_line()
        if data:
            print(f"受信データ: {data.decode('utf-8', errors='ignore').strip()}")
    else:
        print("接続できませんでした")
```

## 貢献

バグ報告や機能リクエストは、GitHubのIssueトラッカーで受け付けています。
プルリクエストも歓迎します。

## ライセンス

RINGOはMITライセンスの下で公開されています。詳細は[LICENSE](../LICENSE)ファイルを参照してください。
