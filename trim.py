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
    # 矩形描画用 クラス変数郡
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    length_x = 0
    length_y = 0
    coor_x = 0
    coor_y = 0

    # テキスト描画用 クラス変数群
    text_offset = 10
    baseline = 0
    baseline_upper = 0
    text1 = "Select area: Drag center"
    text2 = "Quit: Long press \"Esc\" key"
    text3 = "Save: Long press \"s\" key"

    # その他 クラス変数郡
    save_flg = False
    window_name = "Original image"

    def __init__(self, img, save_name):
        self.img = img
        self.save_name = save_name
        self.image = cv2.imread(self.img, 1)
        self.size = self.image.shape

    def start_trim(self):
        u""" トリミング 開始 """
        cv2.namedWindow(Trim.window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(Trim.window_name, self.mouse_event)

        # 読込み画像の大きさから文字描画のベースライン 取得
        Trim.baseline = self.size[0] - Trim.text_offset

        # 操作方法説明文 表示
        text_height = self.write_text(Trim.text1, (1, Trim.baseline))
        Trim.baseline_upper = text_height[1] + Trim.text_offset / 2
        self.write_text(Trim.text2, (1, Trim.baseline_upper))

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
            Trim.save_flg is False
            # テスト出力
            print "Start: " + str(Trim.start_x) + ", " + str(Trim.start_y)

        elif event == cv2.EVENT_LBUTTONUP:
            Trim.end_x, Trim.end_y = Trim.coor_x, Trim.coor_y
            self.image = cv2.imread(self.img, 1)

            # 操作方法説明文 表示
            text_height = self.write_text(Trim.text1, (1, Trim.baseline))
            self.write_text(Trim.text2, (1, Trim.baseline_upper))
            baseline_mid =\
                Trim.baseline - (text_height[1] + Trim.text_offset)
            self.write_text(Trim.text3, (1, baseline_mid))

            # 矩形 描画
            self.draw_rectangle()

            cv2.imshow(Trim.window_name, self.image)
            Trim.save_flg is True

            # テスト出力
            print "End: " + str(Trim.end_x) + ", " + str(Trim.end_y)
            print "Trim area: (" + str(Trim.start_x) + ", "\
                + str(Trim.start_y) + "), ("\
                + str(Trim.end_x) + ", "\
                + str(Trim.end_y) + ")"

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            """ 古い矩形描画を消去するため
            マウス移動イベント毎に対象画像を読込み """
            self.image = cv2.imread(self.img, 1)

            # 矩形 描画
            self.draw_rectangle()

            cv2.imshow(Trim.window_name, self.image)

            # テスト出力
            print "Select: " + str(Trim.coor_x) + ", " + str(Trim.coor_y)

        # 2016/05/24 ここまで！！！ s押下したら終了する！！！
        if cv2.waitKey(33) == ord("s") and Trim.save_flg is True:
            height = 0
            width = 0
            trim_image =\
                self.image[height: Trim.start_y + Trim.length_y,
                        width: Trim.start_x + Trim.length_x]
            cv2.imwrite(Trim.save_name, trim_image)

        return Trim.start_x, Trim.start_y, Trim.end_x, Trim.end_y

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
        Trim.length_x = 2 * Trim.start_x - Trim.coor_x
        Trim.length_y = 2 * Trim.start_y - Trim.coor_y
        start_point = (Trim.length_x, Trim.length_y)
        end_point = (Trim.coor_x, Trim.coor_y)
        color_out = (0, 0, 31)
        color_in = (0, 127, 255)
        thickness_out = 2
        thickness_in = 1
        cra(self.image, start_point, end_point, color_out, thickness_out)
        cra(self.image, start_point, end_point, color_in, thickness_in)


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
