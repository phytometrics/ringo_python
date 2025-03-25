@echo off
REM RINGOパッケージをビルドしてインストールするバッチファイル

echo RINGOパッケージのビルドとインストールを開始します...

REM 現在のディレクトリがスクリプトのあるディレクトリであることを確認
cd /d "%~dp0"

REM 以前のビルドファイルを削除
echo 以前のビルドファイルをクリーンアップしています...
if exist build\ rmdir /s /q build
if exist dist\ rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM パッケージをビルド
echo パッケージをビルドしています...
python setup.py sdist bdist_wheel

REM パッケージをインストール
echo パッケージをインストールしています...
pip install --upgrade dist\*.whl

echo インストールが完了しました。
echo 以下のコマンドでインポートできることを確認してください：
echo python -c "import ringo; print(ringo.__version__)"

pause