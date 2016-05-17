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
    def __init__(self, image):
        self.image = image

    def start_trim(self):
        u""" トリミング 開始 """
        image = cv2.imread(self.image, 1)
        window_name = "Original image"

        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(window_name, self.mouse_event)
        cv2.imshow(window_name, image)
        tpm.termination(0, 0)

    def mouse_event(self, event, coor_x, coor_y, flags, param):
        u""" マウスイベント 取得 """
        start_x = start_y = end_x = end_y = 0

        if event == cv2.EVENT_LBUTTONDOWN:
            # """ 2回目以降に古い描画を消去するため
            # FIXME: 別のウィンドウが生成される！！！
            # 左クリック押下毎に対象画像を読込み """
            # image = cv2.imread(self.image, 1)
            # cv2.imshow("Trimming", image)

            start_x, start_y = coor_x, coor_y
            print "Start trim: " + str(start_x) + ", " + str(start_y)

        if event == cv2.EVENT_LBUTTONUP:
            end_x, end_y = coor_x, coor_y
            end_x = coor_x
            end_y = coor_y
            print "End trim: " + str(end_x) + ", " + str(end_y)

        if event == cv2.EVENT_MOUSEMOVE \
                and flags == cv2.EVENT_FLAG_LBUTTON:
            print "Select: " + str(coor_x) + ", " + str(coor_y)

        if cv2.waitKey(33) > 0:
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
