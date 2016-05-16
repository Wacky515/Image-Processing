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

    def mouse_event(self, event, coor_x, coor_y, flags):
        u""" マウスイベント 取得 """
        if event == cv2.EVENT_LBUTTONDOWN:
            coor_x, coor_y = 0

        if event == cv2.EVENT_MOUSEMOVE:
            print "Selected positon:" + str(coor_x) + ", " + str(coor_y)
            if cv2.waitkey(33) > 0:
                print("Quit")
                tpm.termination(0, 0)

        # if event == cv2.EVENT_LBUTTONDOWN:
# 左クリック押下 画像再描画（いらない表示を消す＝文字のない画像を受け取る！！）
        # image = cv2.imread("***.png")


def main():
    u""" メインルーチン """
    print os.getcwd()
    os.chdir("D:\OneDrive\Biz\Python\ImageProcessing")
    print os.getcwd()

    tm = Trim("trim_test.png")
    tm.start_trim()

if __name__ == '__main__':
    main()
