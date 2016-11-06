# !/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        guitplmatching.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     27/06/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10003
# -----------------------------------------------------------------------------
""" 画像処理 GUI """

# モジュール インポート
import sys
import pickle
import Tkinter as tk
from pprint import pprint

import tplmatching as tm

# sysモジュール リロード
reload(sys)

# デフォルトの文字コード 出力
sys.setdefaultencoding("utf-8")

print_col = 50

# デフォルトのパラメタ
port = 1
model = "C597A"
save_desti = "LABEL BATT-C597A/OTCA-S1P"
barcode = {"C597A": {
            "LABEL BATT-C597A/J-CA": "1AG6P4S2000-ABA",
            "LABEL BATT-C597A/C-CA": "1AG6P4S2000-BBA",
            "LABEL BATT-C597A/OTCA-S1P": "1AG6P4S2000--BA"
            }}

destinations = (barcode[model].keys())

print("Default COM: {}".format(port))
print("".center(print_col, "-"))
print("Default destinations")
pprint(destinations)
print("".center(print_col, "-"))

# パラメタ 読込み
try:
    with open("setting.dump", "r") as load_file:
        load = pickle.load(load_file)
    port = load["port"]
    model = load["model"]
    save_desti = load["save_desti"]
    barcode = load["barcode"]

    print("Load COM: {}".format(port))
    print("Load model: {}".format(model))
    print("Load destination: {}".format(save_desti))
    print("Load barcode: {}".format(barcode))

except:
    print("Save is not found")


def run(event):
    print("START")

    # "port" 入力値をInt型に変換 取得
    port = int(port_txt_fld.get())
    print("")
    print("".center(print_col, "-"))
    print("INFORMATION".center(print_col, " "))
    print("".center(print_col, "-"))
    print("Set COM: {}".format(port))

    # 選択した仕向地 取得
    if val.get() != 0:
        set_desti = val.get()
    else:
        set_desti = save_desti
    # save_desti = val.get()
    print("Get from button: {}".format(val.get()))
    print("Destination: {}".format(set_desti))
    print("".center(print_col, "-"))
    print("INFORMATION".center(print_col, " "))
    print("")

    # パラメタ 保存
    save = {"port": port, "model": model,
            "save_desti": set_desti, "barcode": barcode}
    with open("setting.dump", "wb") as save_file:
        pickle.dump(save, save_file)

    # 画像処理
    cip = tm.ImageProcessing()
    cip.run("Raw capture", "masterImage", port, barcode,
            model=model, destination=set_desti)
            # model=model, destination="LABEL BATT-C597A/OTCA-S1P")
    print("")
    print("GUI image processing end...")
    sys.exit("Image prosedding done")

tki = tk.Tk()
# ウィンドウとタイトル 生成
tki.title("Image process setting")
tki.geometry("400x300")

# ラベル 生成
port_label = tk.Label(text="Input barcode printer's COM port")
# port_label = tk.Label(text="port_label", foreground="#ff0000",
# background="#ffaacc")
port_label.pack()
# port_label.place(x=x座標, y=y座標)  # 描画位置の指定

# テキストフィールド 生成
port_txt_fld = tk.Entry()
# port_txt_fld = tk.Entry(width=50)
port_txt_fld.insert(tk.END, port)
port_txt_fld.pack()

# ラベル 生成
port_label = tk.Label(text="")
port_label.pack()

# ボタン 生成
start_btton = tk.Button(text="START")
start_btton.bind("<Button-1>", run)
start_btton.pack()

# ラベル 生成
port_label = tk.Label(text="")
port_label.pack()
port_label = tk.Label(text="Select destination")
port_label.pack()
port_label = tk.Label(text="")
port_label.pack()

# ラジオボタン 生成
val = tk.StringVar()
# 初期"ON"状態のボタン
val.set(save_desti)

# 仕向け地数のラジオボタン 生成
for destination in destinations:
    print("{}, {}".format(save_desti, destination))
    desti_radio = tk.Radiobutton(text=destination, variable=val,
                                 value=destination)
    desti_radio.pack()

tki.mainloop()


def main():
    sys.path.append("D:\OneDrive\Biz\Python\ImageProcess")

if __name__ == "__main__":
    main()
