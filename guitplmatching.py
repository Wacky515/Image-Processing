# !/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        guitplmatching.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     2016/06/27
# Last Change: 2021/03/14 23:33:57.
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10003
# -----------------------------------------------------------------------------
""" 画像処理 GUI """

# モジュール インポート
import sys
import pickle
import importlib

# MEMO: "Python3" は "tkinter"
if sys.version_info.major == 3:
    import tkinter as tk
elif sys.version_info.major == 2:
    import Tkinter as tk
    # Python2 用設定
    # sysモジュール リロード
    importlib.reload(sys)
    # デフォルトの文字コード 出力
    sys.setdefaultencoding("utf-8")

import tplmatching as tm


print_col = 50

# デフォルトのパラメタ
val_ok = 80
obj_detect = 40
# port = 1  # {{{
# model = "C597A"
# save_desti = "LABEL BATT-C597A/OTCA-S1P"
# barcode = {"C597A": {
#             "LABEL BATT-C597A/J-CA": "1AG6P4S2000-ABA",
#             "LABEL BATT-C597A/C-CA": "1AG6P4S2000-BBA",
#             "LABEL BATT-C597A/OTCA-S1P": "1AG6P4S2000--BA"
#             }}
# destinations = (barcode[model].keys()
# )}}}

print("Default OK value: {}".format(val_ok))
print("Default search mode value: {}".format(obj_detect))
# print("Default COM: {}".format(port))  # {{{
# print("".center(print_col, "-"))
# print("Default destinations")
# pprint(destinations)
# print("".center(print_col, "-"))
# }}}

# パラメタ 読込み
try:
    with open("setting.dump", "rb") as load_file:
        load = pickle.load(load_file)
    val_ok = load["val_ok"]
    obj_detect = load["obj_detect"]
    # port = load["port"]  # {{{
    # model = load["model"]
    # save_desti = load["save_desti"]
    # barcode = load["barcode"]
# }}}

    print("Load OK value: {}".format(val_ok))
    print("Load search mode value: {}".format(obj_detect))
    # print("Load COM: {}".format(port))  # {{{
    # print("Load model: {}".format(model))
    # print("Load destination: {}".format(save_desti))
    # print("Load barcode: {}".format(barcode))
# }}}

except OSError:
    print("Not found setting.dump")


def run(event):
    print("".center(print_col, "-"))
    print(" START ")
    print("".center(print_col, "-"))
    print("")

    # "val_ok" 入力値をInt型に変換 取得
    val_ok = int(val_ok_txt_fld.get())
    # "val_ok" 入力値制限
    if val_ok < 10:
        val_ok = 10
    elif val_ok > 99:
        val_ok = 99

    # "obj_detect" 入力値をInt型に変換 取得
    obj_detect = int(obj_detect_txt_fld.get())
    # "obj_detect" 入力値制限
    if obj_detect < 0:
        obj_detect = 0
    elif obj_detect > 70:
        obj_detect = 70
    elif obj_detect > val_ok:
        obj_detect = val_ok - 1

    # "port" 入力値をInt型に変換 取得  # {{{
    # port = int(port_txt_fld.get())
    # }}}

    print("")
    print("".center(print_col, "-"))
    print(" INFORMATION ".center(print_col, " "))
    print("".center(print_col, "-"))
    print("Set OK value: {}".format(val_ok))
    print("Set search mode value: {}".format(obj_detect))
    print("")
    # print("Set COM: {}".format(port))

    # # 選択した仕向地 取得  # {{{
    # if val.get() != 0:
    #     set_desti = val.get()
    # else:
    #     set_desti = save_desti
    # # save_desti = val.get()
    # print("Get from button: {}".format(val.get()))
    # print("Destination: {}".format(set_desti))
    # }}}

    print("".center(print_col, "-"))
    print(" INFORMATION ".center(print_col, " "))
    print("")

    # パラメタ 保存
    with open("setting.dump", "wb") as save_file:
        save = {"val_ok": val_ok, "obj_detect": obj_detect}
    #   save = {"port": port, "model": model,  # {{{
    #         "save_desti": set_desti, "barcode": barcode
    # }}}}
        pickle.dump(save, save_file)

    # 画像処理
    cip = tm.ImageProcessing()
    cip.run("Raw capture", "masterImage", val_ok=val_ok / 100,
            obj_detect=obj_detect / 100)
    print("")
    print("GUI image processing end...")
    sys.exit("Image prosedding done")


tki = tk.Tk()

# ウィンドウとタイトル 生成
tki.title("Setting image processing")
tki.geometry("400x300")

# ラベル 生成
val_ok_label = tk.Label(text="Input judge OK value [10~99]%")
val_ok_label.pack()

# テキストフィールド 生成
val_ok_txt_fld = tk.Entry()
# val_ok_txt_fld = tk.Entry(width=50)
val_ok_txt_fld.insert(tk.END, val_ok)
val_ok_txt_fld.pack()

# ラベル 生成
val_ok_label = tk.Label(text="")
val_ok_label.pack()

# ラベル 生成
obj_detect_label = tk.Label(text="Input shift serarch mode value [0~70]%")
obj_detect_label.pack()
obj_detect_caution_label = tk.Label(text="This value must be lower OK value")
obj_detect_caution_label.pack()

# テキストフィールド 生成
obj_detect_txt_fld = tk.Entry()
obj_detect_txt_fld.insert(tk.END, obj_detect)
obj_detect_txt_fld.pack()

# ラベル 生成
obj_detect_label = tk.Label(text="")
obj_detect_label.pack()

# ボタン 生成
start_btton = tk.Button(text="INPUT")
start_btton.bind("<Button-1>", run)
start_btton.pack()

# # ラベル 生成  # {{{
# port_label = tk.Label(text="Input barcode printer's COM port")
# port_label.pack()

# # テキストフィールド 生成
# port_txt_fld = tk.Entry()
# # port_txt_fld = tk.Entry(width=50)
# port_txt_fld.insert(tk.END, port)
# port_txt_fld.pack()

# # ラベル 生成
# port_label = tk.Label(text="")
# port_label.pack()

# # ボタン 生成
# start_btton = tk.Button(text="START")
# start_btton.bind("<Button-1>", run)
# start_btton.pack()

# # ラベル 生成
# port_label = tk.Label(text="")
# port_label.pack()
# port_label = tk.Label(text="Select destination")
# port_label.pack()
# port_label = tk.Label(text="")
# port_label.pack()

# # ラジオボタン 生成
# val = tk.StringVar()
# # 初期"ON"状態のボタン
# val.set(save_desti)

# # 仕向け地数のラジオボタン 生成
# for destination in destinations:
#     print("{}, {}".format(save_desti, destination))
#     desti_radio = tk.Radiobutton(text=destination, variable=val,
#                                  value=destination)
#     desti_radio.pack()
# }}}

tki.mainloop()


def main():
    sys.path.append("D:\\OneDrive\\Biz\\Python\\ImageProcess")


if __name__ == "__main__":
    main()
