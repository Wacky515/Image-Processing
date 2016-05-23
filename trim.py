# --------------------------------------------------
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
# Gdiff test 2016/05/11

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
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    coor_x = 0
    coor_y = 0
    window_name = "Original image"
    baseline = 0

    def __init__(self, img):
        self.img = img
        self.image = cv2.imread(self.img, 1)
        self.size = self.image.shape

    def start_trim(self):
        u""" トリミング 開始 """
        cv2.namedWindow(Trim.window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(Trim.window_name, self.mouse_event)

        # 読込み画像の大きさ 取得
        Trim.baseline = self.size[0] - 10

        # 操作方法説明文 表示
        self.write_text("Select area: Drag center", (1, Trim.baseline))
        # text_height = self.write_text("Select Area:Drag center", (1, baseline))
        # baseline_upper = baseline - text_height[1] - 3
        # self.write_text("Captcha:Long press S", (1, baseline_upper))

        cv2.imshow(Trim.window_name, self.image)
        # テスト出力
        print "Trim pos: (" + str(Trim.start_x) + ", "\
                + str(Trim.start_y) + "), ("\
                + str(Trim.end_x) + ", "\
                + str(Trim.end_y) + ")"

        tpm.termination(0, 0)

    def mouse_event(self, event, coor_x, coor_y, flags, param):
        u""" マウスイベント 取得 """
        Trim.coor_x = coor_x
        Trim.coor_y = coor_y

        if event == cv2.EVENT_LBUTTONDOWN:
            Trim.start_x = Trim.start_y = Trim.end_x = Trim.end_y = 0
            """ 2回目以降に古い描画を消去するため
            左クリック押下毎に対象画像を読込み """
            self.image = cv2.imread(self.img, 1)

            Trim.start_x, Trim.start_y = Trim.coor_x, Trim.coor_y
            print "Start: " + str(Trim.start_x) + ", " + str(Trim.start_y)

        elif event == cv2.EVENT_LBUTTONUP:
            Trim.end_x, Trim.end_y = Trim.coor_x, Trim.coor_y
            # 2016/05/23 ここまで！！！ "s"キーで画像保存処理実装から

            print "End: " + str(Trim.end_x) + ", " + str(Trim.end_y)
            print "Trim area: (" + str(Trim.start_x) + ", "\
                    + str(Trim.start_y) + "), ("\
                    + str(Trim.end_x) + ", "\
                    + str(Trim.end_y) + ")"

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            """ 古い矩形描画を消去するため
            マウス移動イベント毎に対象画像を読込み """
            self.image = cv2.imread(self.img, 1)

            cra = cv2.rectangle
            length_x = 2 * Trim.start_x - Trim.coor_x
            length_y = 2 * Trim.start_y - Trim.coor_y
            start_point = (length_x, length_y)
            end_point = (Trim.coor_x, Trim.coor_y)
            color_out = (0, 0, 31)
            color_in = (0, 127, 255)
            thickness_out = 2
            thickness_in = 1
            cra(self.image, start_point, end_point, color_out, thickness_out)
            cra(self.image, start_point, end_point, color_in, thickness_in)
            cv2.imshow(Trim.window_name, self.image)

            # 2016/05/23 ここまで2！！！
            # self.write_text("Save: Long press \"s\" key", (1, Trim.baseline))

            print "Select: " + str(Trim.coor_x) + ", " + str(Trim.coor_y)

        elif cv2.waitKey(33) > 0:
            print("Quit")
            tpm.termination(0, 0)

        return Trim.start_x, Trim.start_y, Trim.end_x, Trim.end_y

    def write_text(self, text, origin,
            scale=0.7,
            color_out=(0, 0, 31), color_in=(0, 127, 225),
            thickness_out=3, thickness_in=1):
        u""" テキスト 画面出力 """
        cpt = cv2.putText
        image = self.image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cpt(image, text, origin, font, scale, color_out, thickness_out)
        cpt(image, text, origin, font, scale, color_in, thickness_in)
        # 戻り値にフォントサイズを指定
        size, baseline = cv2.getTextSize(text, font, scale, thickness_out)
        return size


def main():
    u""" メインルーチン """
    print os.getcwd()
    os.chdir("D:\OneDrive\Biz\Python\ImageProcessing")
    print os.getcwd()

    tm = Trim("trim_test.png")
    # tm = Trim("trim_test2.png")
    tm.start_trim()

if __name__ == '__main__':
    main()
