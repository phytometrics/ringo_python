#!/bin/bash

# RINGOパッケージをビルドしてインストールするスクリプト

echo "RINGOパッケージのビルドとインストールを開始します..."

# 現在のディレクトリがスクリプトのあるディレクトリであることを確認
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 以前のビルドファイルを削除
echo "以前のビルドファイルをクリーンアップしています..."
rm -rf build/ dist/ *.egg-info/

# パッケージをビルド
echo "パッケージをビルドしています..."
python setup.py sdist bdist_wheel

# パッケージをインストール
echo "パッケージをインストールしています..."
pip install --upgrade dist/*.whl

echo "インストールが完了しました。"
echo "以下のコマンドでインポートできることを確認してください："
echo "python -c 'import ringo; print(ringo.__version__)'"