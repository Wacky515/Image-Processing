# IMAGE PROCESSING

## MEMO

### PyInstaller

- 変換元の \*.py のディレクトリに自作モジュールのシンボリックリンクを設置
- "miniconda" で仮想環境を構築する
  - 仮想環境名: image-processing
- 仮想環境に入室し関係するモジュールを "pip install *" する
  - モジュール: pyinstaller opencv-python numpy
- 仮想環境で \*.exe 化する \*.py のあるディレクトリに cd
- 仮想環境で `pyinstaller *.py --onefile` 実行
