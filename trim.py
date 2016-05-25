﻿# --------------------------------------------------
# Name:        trim.py
# Purpose:     Trimming master image
#
# Author:      Kilo11
#
# Created:     03/12/2015
# Copyright:   (c) SkyDog 2015
# Licence:     SDS10002.200
# --------------------------------------------------
u""" 画像のトリミング"""
# !/usr/bin/python
# デフォルトの文字コード 変更
# -*- coding: utf-8 -*-

# モジュール インポート
import numpy as np
import cv2
import cv2.cv as cv
import os
import tplmatching as tpm

import sys
# sysモジュール リロード
reload(sys)

# デフォルトの文字コード 出力
sys.setdefaultencoding("utf-8")


class Trim:
    u""" トリミング クラス """

    def __init__(self, img, save_name):
        # 画像読込み用 インスタンス変数郡# {{{
        self.img = img
        self.save_name = save_name
        self.image = cv2.imread(self.img, 1)
        self.size = self.image.shape
# }}}

        # 矩形描画用 インスタンス変数郡# {{{
        self.start_x = self.start_y = 0
        self.end_x = self.end_y = 0
        self.length_x = self.length_y = 0
# }}}

        # テキスト描画用 インスタンス変数郡# {{{
        self.text_offset = 10
        self.baseline = 0
        self.baseline_upper = 0
        self.text1 = "Select area: Drag center"
        self.text2 = "Quit: Long press \"q\" key"
        self.text3 = "Save: Long press \"s\" key"
# }}}

        # その他 インスタンス変数郡# {{{
        self.window_name = "Original image"
        self.save_flg = False
        self.save_key = "s"
        self.quit_key = "q"
# }}}

    def start_trim(self):
        u""" トリミング 開始 """
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(self.window_name, self.mouse_event)

        # 読込み画像の大きさから文字描画のベースライン 取得
        self.baseline = self.size[0] - self.text_offset

        # 操作方法説明文 表示
        text_height = self.write_text(self.text1, (1, self.baseline))
        self.baseline_upper = text_height[1] + self.text_offset / 2
        self.write_text(self.text2, (1, self.baseline_upper))

        cv2.imshow(self.window_name, self.image)

        # テスト出力
        print "Trim pos: (" + str(self.start_x) + ", "\
            + str(self.start_y) + "), ("\
            + str(self.end_x) + ", "\
            + str(self.end_y) + ")"

        self.quit_tirm()

        print "Code end"
        # 静止画の出力保持処理
        # tpm.termination(0, 0)

    def mouse_event(self, event, coor_x, coor_y, flags, param):
        u""" マウスイベント 取得 """
        self.coor_x = coor_x
        self.coor_y = coor_y

        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_x = self.start_y = self.end_x = self.end_y = 0
            """ 2回目以降に古い描画を消去する為
            左クリック押下毎に対象画像を読込み """
            self.image = cv2.imread(self.img, 1)

            self.start_x, self.start_y = self.coor_x, self.coor_y
            self.save_flg = False

            # テスト出力
            print "Left button down"
            print "Start: " + str(self.start_x) + ", " + str(self.start_y)

        elif event == cv2.EVENT_LBUTTONUP:
            self.end_x, self.end_y = self.coor_x, self.coor_y
            self.image = cv2.imread(self.img, 1)

            # 操作方法説明文 表示
            text_height = self.write_text(self.text1, (1, self.baseline))
            self.write_text(self.text2, (1, self.baseline_upper))
            baseline_mid =\
                self.baseline - (text_height[1] + self.text_offset)
            self.write_text(self.text3, (1, baseline_mid))

            # 矩形 描画
            self.draw_rectangle()

            cv2.imshow(self.window_name, self.image)
            self.save_flg = True

            # テスト出力
            print "Left button up"
            print "End: " + str(self.end_x) + ", " + str(self.end_y)
            print "Trim area: (" + str(self.start_x) + ", "\
                + str(self.start_y) + "), ("\
                + str(self.end_x) + ", "\
                + str(self.end_y) + ")"
            print self.save_flg

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            """ 古い矩形描画を消去する為
            マウス移動イベント毎に対象画像を読込み """
            self.image = cv2.imread(self.img, 1)

            # 矩形 描画
            self.draw_rectangle()

            cv2.imshow(self.window_name, self.image)

            # テスト出力
            print "Mouse location: " + str(self.coor_x) + ", "\
                + str(self.coor_y)

        if cv2.waitKey(0) == ord(self.save_key) and self.save_flg is True:
            # テスト出力
            print "Input key \"s\""
            print "Save image..."
            print "Trim range: (" + str(self.start_x) + ", "\
                + str(self.start_y) + "), ("\
                + str(self.length_x) + ", "\
                + str(self.length_y) + ")"

            # 各種描画を消去する為 対象画像を再読込み
            self.image = cv2.imread(self.img, 1)

            # 2016/05/25 AM ここまで トリミング範囲演算 途中！！！
            # トリミング範囲 演算
            height = self.start_y - self.length_y / 2
            width = self.start_x - self.length_x / 2
            trim_image = self.image[height: height + self.length_y,
                width: width + self.length_x]

            # 保存処理と保存フラグ偽処理
            cv2.imwrite(self.save_name, trim_image)
            self.save_flg = False

        self.quit_tirm()

    def write_text(self, text, origin,
            cpt=cv2.putText,
            scale=0.7,
            color_out=(0, 0, 31), color_in=(0, 127, 225),
            thickness_out=3, thickness_in=1):
        u""" テキスト 画面出力 """
        image = self.image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cpt(image, text, origin, font, scale, color_out, thickness_out)
        cpt(image, text, origin, font, scale, color_in, thickness_in)
        # 戻り値にフォントサイズを指定
        size, baseline = cv2.getTextSize(text, font, scale, thickness_out)
        return size

    def draw_rectangle(self):
        u""" 矩形 描画 """
        cra = cv2.rectangle
        self.length_x = 2 * self.start_x - self.coor_x
        self.length_y = 2 * self.start_y - self.coor_y
        start_point = (self.length_x, self.length_y)
        end_point = (self.coor_x, self.coor_y)
        color_out = (0, 0, 31)
        color_in = (0, 127, 255)
        thickness_out = 2
        thickness_in = 1
        cra(self.image, start_point, end_point, color_out, thickness_out)
        cra(self.image, start_point, end_point, color_in, thickness_in)

    def quit_tirm(self):
        # 静止画の出力保持&終了処理
        if cv2.waitKey(0) == ord(self.quit_key):
            # テスト出力
            print "Input key \"q\""
            print "Quit"
            cv2.destroyWindow(self.window_name)
            sys.exit()


def main():
    u""" メインルーチン """
    print os.getcwd()
    os.chdir("D:\OneDrive\Biz\Python\ImageProcessing")
    print os.getcwd()

    tm = Trim("trim_test.png", "trimed.png")
    # tm = Trim("trim_test2.png")
    tm.start_trim()

if __name__ == '__main__':
    main()

""" FIXME:
RuntimeError: maximum recursion depth exceeded. 再帰の回数の限界を超えている
→ トリミングモードの開始回数を制限する！！！
"""
