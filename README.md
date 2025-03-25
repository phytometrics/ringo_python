# RINGO_python

シリアル通信を簡単に扱うためのPythonラッパーライブラリ

## 概要

RINGO_pythonは、Pythonの`pyserial`ライブラリを使用して、シリアル通信を簡単に行うためのラッパークラスを提供します。エラー処理やログ記録、コンテキストマネージャのサポートなど、シリアル通信を扱う際の一般的な機能を備えています。

## 機能

- シリアルポートへの接続・切断
- データの送受信
- エラー処理とログ記録
- コンテキストマネージャのサポート（`with`文での使用）
- 再接続機能

## インストール

### pipを使用したインストール

```bash
pip install ringo
```

### ソースからのインストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/RINGO_python.git
cd RINGO_python/ringo

# インストール
pip install -e .
```

または、提供されているスクリプトを使用：

Linux/Mac:

```bash
cd ringo
./build_and_install.sh
```

Windows:

```
cd ringo
build_and_install.bat
```

## 使用方法

### 基本的な使い方

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

### 手動での接続・切断

```python
from ringo import SerialSensorWrapper

# インスタンスを作成
sensor = SerialSensorWrapper("/dev/ttyUSB0", baudrate=115200)

# 接続
sensor.open()

if sensor.is_connected():
    # データを送信
    sensor.write_data("COMMAND\r\n")
    
    # データを受信
    data = sensor.read_line()
    if data:
        print(f"受信データ: {data.decode('utf-8', errors='ignore').strip()}")
else:
    print("接続できませんでした")

# 切断
sensor.close()
```

## プロジェクト構造

```
RINGO_python/
├── main.py                  # オリジナルのソースコード
├── ringo/                   # パッケージディレクトリ
│   ├── ringo/
│   │   ├── __init__.py      # パッケージ初期化ファイル
│   │   └── serial_wrapper.py # シリアル通信ラッパークラス
│   ├── setup.py             # パッケージインストール設定
│   ├── README.md            # パッケージの概要
│   ├── LICENSE              # MITライセンス
│   ├── build_and_install.sh # Linux/Mac用ビルド・インストールスクリプト
│   └── build_and_install.bat # Windows用ビルド・インストールスクリプト
├── docs/                    # ドキュメントディレクトリ
│   ├── index.md             # ドキュメントインデックス
│   ├── installation.md      # インストールガイド
│   ├── api_reference.md     # APIリファレンス
│   ├── examples.md          # 使用例
│   └── troubleshooting.md   # トラブルシューティングガイド
└── README.md                # このファイル
```

## ドキュメント

詳細なドキュメントは`docs`ディレクトリにあります：

- [インストールガイド](docs/installation.md)
- [APIリファレンス](docs/api_reference.md)
- [使用例](docs/examples.md)
- [トラブルシューティング](docs/troubleshooting.md)

## 依存パッケージ

- pyserial >= 3.4

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](ringo/LICENSE)ファイルを参照してください。

## 貢献

バグ報告や機能リクエストは、GitHubのIssueトラッカーで受け付けています。
プルリクエストも歓迎します。
