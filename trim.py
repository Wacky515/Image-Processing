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
    coor_x = 0
    coor_y = 0

    def __init__(self, img):
        self.img = img
        self.image = cv2.imread(self.img, 1)

    def start_trim(self):
        u""" トリミング 開始 """
        window_name = "Original image"

        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(window_name, self.mouse_event)
        cv2.imshow(window_name, self.image)
        tpm.termination(0, 0)

    def mouse_event(self, event, coor_x, coor_y, flags, param):
        u""" マウスイベント 取得 """
        Trim.coor_x = coor_x
        Trim.coor_y = coor_y

        if event == cv2.EVENT_LBUTTONDOWN:
            Trim.start_x = Trim.start_y = end_x = end_y = 0
            """ 2回目以降に古い描画を消去するため
            左クリック押下毎に対象画像を読込み """
            self.image = cv2.imread(self.img, 1)

            Trim.start_x, Trim.start_y = Trim.coor_x, Trim.coor_y
            print "Start: " + str(Trim.start_x) + ", " + str(Trim.start_y)

        elif event == cv2.EVENT_LBUTTONUP:
            end_x, end_y = Trim.coor_x, Trim.coor_y
            print "End: " + str(end_x) + ", " + str(end_y)

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            """ 古い矩形描画を消去するため
            マウス移動イベント毎に対象画像を読込み """
            self.image = cv2.imread(self.img, 1)
            cra = cv2.rectangle
            length_x = 2 * Trim.start_x - Trim.coor_x
            length_y = 2 * Trim.start_y - Trim.coor_y
            start_point = (length_x, length_y)
            end_point = (Trim.coor_x, Trim.coor_y)
            color = (0, 127, 255)
            thickness = 2
            cra(self.image, start_point, end_point, color, thickness)

            # FIXME: 矩形描画が別ウインドウになる！！！
            cv2.imshow("Trim", self.image)

            print "Select: " + str(Trim.coor_x) + ", " + str(Trim.coor_y)

        elif cv2.waitKey(33) > 0:
            print("Quit")
            tpm.termination(0, 0)


def main():
    u""" メインルーチン """
    print os.getcwd()
    os.chdir("D:\OneDrive\Biz\Python\ImageProcessing")
    print os.getcwd()

    tm = Trim("trim_test.png")
    tm.start_trim()

if __name__ == '__main__':
    main()
