# !/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------  # {{{
# Name:        trim.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     2015/12/03 **:**:**
# Last Change: 2021/04/30 10:27:35.
# Copyright:   (c) SkyDog 2015
# Licence:     SDS10002
# ----------------------------------------------------------------------  # }}}
""" 画像のトリミング処理 """

# TODO:
#    単体で動作できるようにする
#    変数は "[大区分/固有]_[小区分/汎用]"

# FIXME:
#    "Linux" でトリム画像が保存できない
#    print("Quit trim mode") がループする
#    ただし、実用上は支障なし

#    RuntimeError: maximum recursion depth exceeded.
#    再帰の回数の限界を超えている
#    → トリミングモードの開始回数を制限する！！！
#    → 一枚の画像から複数枚保存できる機能は残す（安易に Save -> 終了にしない）

# DONE:

# モジュール インポート  # {{{
import os
import sys
import cv2
import time
import platform
import importlib
import savedata as sd
# from pprint import pprint

# Python2 用設定
if sys.version_info.major == 2:
    # MEMO:
    #   Python3系ではデフォルトエンコードがutf-8のため、
    #   sys.setdefaultencoding('UTF8')は非推奨
    #   sysモジュール リロード
    importlib.reload(sys)
    # デフォルトの文字コード 出力
    sys.setdefaultencoding("utf-8")

# カレントディレクトリに CD して、並列にある自作モジュールパスを追加
wdir = os.path.abspath(os.path.dirname(__file__))
os.chdir(wdir)

sys.path.append(os.path.join("..", "SaveData"))
# }}}

print_col = 50


class Trim:
    """ トリミング クラス """

    def __init__(self, img, name, extension, path, _type=0, end_process=0):
        # 画像読込み用 インスタンス変数  # {{{
        # _type: 0: 静止画 1: 動画 切換え
        self.img = img
        self.name = name
        self.extension = extension
        self.path = path

        if _type == 0:
            self.image = cv2.imread(self.img, 1)
            self.size = self.image.shape
        else:
            self.image = img

        self.end_process = end_process
        # }}}

        # 矩形描画用 インスタンス変数  # {{{
        self.start_x = self.start_y = 0
        self.end_x = self.end_y = 0
        self.length_x = self.length_y = 0
        # }}}

        # テキスト描画用 インスタンス変数  # {{{
        self.text_offset = 10
        self.baseline = 0
        self.baseline_upper = 0
        self.text1 = "Select area: Drag center"
        self.text2 = "Quit: Long press \"q\" key"
        self.text3 = "Save: Long press \"s\" key"
        # }}}

        # その他 インスタンス変数  # {{{
        self.window_name = "Original image"
        self.save_flag = False

        # "Linux" のキーイン差異 補完
        if platform.system() == "Linux":
            self.key_save = 1048691
            self.key_quit = 1048689
        else:
            self.key_save = ord("s")
            self.key_quit = ord("q")
        # }}}

    def trim(self):
        """ トリミング 処理 """
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(self.window_name, self.mouse_event)

        # 読込み画像の大きさから文字描画のベースライン 取得
        self.baseline = self.size[0] - self.text_offset

        # 操作方法説明文 表示
        text_height = self.write_text(self.text1, (1, self.baseline))
        # self.baseline_upper = text_height[1] + self.text_offset / 2
        self.baseline_upper = text_height[1] + self.text_offset // 2
        self.write_text(self.text2, (1, self.baseline_upper))

        cv2.imshow(self.window_name, self.image)

        ssx = str(self.start_x)
        ssy = str(self.start_y)
        sex = str(self.end_x)
        sey = str(self.end_y)

        print("Trim pos: ({}, {}), ({}, {})".format(ssx, ssy, sex, sey))

        # 保存 処理
        self.save_trim()

        print(">> Trim end...")
        print("")

    def mouse_event(self, event, coor_x, coor_y, flags, param):
        """ マウスイベント 取得 """
        # マウス座標を代入（"__init__" ではない！！！）
        self.coor_x = coor_x
        self.coor_y = coor_y

        # 左クリック押下 処理
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_x = self.start_y = self.end_x = self.end_y = 0
            # 2回目以降に古い描画を消去する為
            # 左クリック押下毎に対象画像を読込み
            self.image = cv2.imread(self.img, 1)

            self.start_x, self.start_y = self.coor_x, self.coor_y
            print(">> Left button down")
            print("")

            self.save_flag = False
            print(">> Save flag is " + str(self.save_flag))
            print(">> Start: " + str(self.start_x) + ", " + str(self.start_y))

        # 左クリック押上 処理
        elif event == cv2.EVENT_LBUTTONUP:
            self.end_x, self.end_y = self.coor_x, self.coor_y
            self.image = cv2.imread(self.img, 1)

            # 操作方法説明文 表示
            text_height = self.write_text(self.text1, (1, self.baseline))
            self.write_text(self.text2, (1, self.baseline_upper))
            baseline_mid = \
                self.baseline - (text_height[1] + self.text_offset)
            self.write_text(self.text3, (1, baseline_mid))

            # 矩形 描画
            self.draw_rectangle()
            cv2.imshow(self.window_name, self.image)

            self.save_flag = True

            ssx = str(self.start_x)
            ssy = str(self.start_y)
            sex = str(self.end_x)
            sey = str(self.end_y)

            print(">> Left button up")
            print(">> End: {}, {}".format(sex, sey))

            print(">> Trim pos: ({}, {}), ({}, {})".format(ssx, ssy, sex, sey))
            print(">> Save flag is " + str(self.save_flag))
            print("")

        # マウス移動 処理
        # FIXME: "Linux" では動作しない
        # FIXED?: "RuntimeError" になる（再帰が深すぎる）！！！
        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            # 古い矩形描画を消去する為
            # マウス移動イベント毎に対象画像を読込み
            self.image = cv2.imread(self.img, 1)

            # 矩形 描画
            self.draw_rectangle()

            cv2.imshow(self.window_name, self.image)

            scx = str(self.coor_x)
            scy = str(self.coor_y)
            print(">> Mouse location: {}, {}".format(scx, scy))

    def write_text(self, text, origin,
                   scale=0.7,
                   color_out=(0, 0, 31), color_in=(0, 127, 225),
                   thickness_out=3, thickness_in=1,
                   offset=(0, 0)):
        """ テキスト 描画 """
        # 色指定のニーモニック 呼出し
        if type(color_out) is str:
            color_out = self.convert_color(color_out)
        if type(color_in) is str:
            color_in = self.convert_color(color_in)

        # 戻り値にフォントサイズを指定
        font = cv2.FONT_HERSHEY_SIMPLEX
        size, baseline = cv2.getTextSize(text, font, scale, thickness_out)

        # 描画y座標が "height" なら文字自体の高さを代入
        if origin[1] == "height":
            # 要素書換えのためタプルをリストに変換後、復元
            origin = list(origin)
            origin[1] = size[1] + offset[1]
            origin = tuple(origin)

        cpt = cv2.putText
        image = self.image
        cpt(image, text, origin, font, scale, color_out, thickness_out)
        cpt(image, text, origin, font, scale, color_in, thickness_in)
        return size

    def draw_rectangle(self,
                       start_point=None, end_point=None,
                       color_out=(0, 0, 31), color_in=(0, 127, 225),
                       thickness_out=2, thickness_in=1):
        """ 矩形 描画 """
        # 色指定のニーモニック 呼出し
        if type(color_out) is str:
            color_out = self.convert_color(color_out)
        if type(color_in) is str:
            color_in = self.convert_color(color_in)

        cra = cv2.rectangle
        if start_point is end_point is None:
            self.length_x = 2 * self.start_x - self.coor_x
            self.length_y = 2 * self.start_y - self.coor_y
            start_point = (self.length_x, self.length_y)
            end_point = (self.coor_x, self.coor_y)
        cra(self.image, start_point, end_point, color_out, thickness_out)
        cra(self.image, start_point, end_point, color_in, thickness_in)

    def convert_color(self, color):
        """ 指定色（ニーモニック） 変換 """
        if color == "red":
            color = (0, 0, 255)
        elif color == "green":
            color = (0, 255, 0)
        elif color == "white":
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)
        return color

    def save_trim(self):
        """ 保存 処理 """
        if cv2.waitKey(0) == self.key_save and self.save_flag is True:
            print(">> Input key \"{}\"".format(self.key_save))
            print(">> Save image...")

            ssx = str(self.start_x)
            ssy = str(self.start_y)
            slx = str(self.length_x)
            sly = str(self.length_y)

            print(">> Save pos: ({}, {}), ({}, {})".format(ssx, ssy, slx, sly))
            print("")

            # 各種描画を消去する為 対象画像を再読込み
            self.image = cv2.imread(self.img, 1)

            # トリミング範囲 演算
            height = self.length_y
            width = self.length_x
            image_trim = self.image[height: self.end_y, width: self.end_x]

            # 保存処理と保存フラグ "真" -> "偽" 処理
            sda = sd.SaveData(self.name, self.path)
            sda.save_image(image_trim, self.extension)

            self.save_flag = False

            # トリムウィンドウ 自動消去
            if self.end_process != 0:
                cv2.destroyAllWindows()
                cv2.imshow("Save image", image_trim)
                time.sleep(1)
                self.quit_tirm(1)

            cv2.imshow("Save image", image_trim)
            time.sleep(0.1)
            self.quit_tirm()

    def quit_tirm(self, mode=0):
        """ 静止画の出力保持 & 終了処理 """
        if mode == 0:
            if cv2.waitKey(0) == self.key_quit:
                time.sleep(0.1)
                print(">> Input key \"{}\"".format(self.key_quit))
                print(">> Quit trim mode by key")

        cv2.destroyAllWindows()
        print(">> Erase window")
        print("")

        return False


def main():
    """ メインルーチン """
    # "Vim" テスト用各変数 定義  # {{{
    # イニシャル情報 出力
    print("".center(print_col, "-"))
    print("INFORMATION INIT".center(print_col, " "))
    print("".center(print_col, "-"))
    print("Default current directory:")
    print(os.getcwd().rjust(print_col, " "))
    print("")

    print(">> Current dir:")
    os.chdir(wdir)
    print(os.getcwd().rjust(print_col, " "))

    # MEMO: 整数演算は "//" を使用する
    #     "/" は浮動小数点を返す
    print(u"〓" * int(print_col // 2))
    # print(u"〓" * int(print_col / 2))
    print("START MAIN".center(print_col, " "))
    print(u"〓" * int(print_col // 2))
    # print(u"〓" * int(print_col / 2))
    print("")
    # }}}

    image = "trim_test.png"
    home_dir = os.path.expanduser("~")

    if os.name == "nt":
        save_dir = ".\\MasterImage"

    elif os.name == "posix":
        print(">> Run in Unix, set save path as Unix")
        save_dir = os.path.join(home_dir, "Python/ImageProcessing/MasterImage")
        print(">> Save dir: " + save_dir)
    else:
        save_dir = "./MasterImage"

    tm = Trim(image, "trimed", ".png", save_dir, end_process=0)
    # tm = Trim(image, "trimed", ".png", save_dir, end_process=1)
    # tm = Trim("trim_test.png", "trimed",
    #           ".png", save_dir, _type=1, end_process=1)
    # tm = Trim("trim_test.png", "trimed", ".png", save_dir)
    # tm = Trim("trim_test2.png")
    tm.trim()


if __name__ == "__main__":
    main()
