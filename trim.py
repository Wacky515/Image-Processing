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
    # 2016/05/19 引数の受渡しができない！！！
    start_x = 0
    start_y = 0
    coor_x = 0
    coor_y = 0

    def __init__(self, img):
    # def __init__(self, img, start_x, start_y, coor_x, coor_y):
        self.img = img
        self.image = cv2.imread(self.img, 1)
        # self.start_x = start_x
        # self.start_y = start_y
        # self.coor_x = coor_x
        # self.coor_y = coor_y

    def start_trim(self):
        u""" トリミング 開始 """
        window_name = "Original image"

        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(window_name, self.mouse_event)
        cv2.imshow(window_name, self.image)
        cra = cv2.rectangle
        cra(self.image,
            (self.start_x, self.start_y),
            (self.coor_x, self.coor_y),
            (255, 0, 0), 3)
        tpm.termination(0, 0)

    def mouse_event(self, event, coor_x, coor_y, flags, param):
        u""" マウスイベント 取得 """
        self.start_x = self.start_y = end_x = end_y = 0

        if event == cv2.EVENT_LBUTTONDOWN:
            # FIXME: 別のウィンドウが生成される！！！
            # """ 2回目以降に古い描画を消去するため
            # 左クリック押下毎に対象画像を読込み """
            # cv2.imshow("Trimming", self.image)

            self.start_x, self.start_y = self.coor_x, self.coor_y
            print "Start: " + str(self.start_x) + ", " + str(self.start_y)

        elif event == cv2.EVENT_LBUTTONUP:
            end_x, end_y = self.coor_x, self.coor_y
            print "End: " + str(end_x) + ", " + str(end_y)

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            # image = cv2.imread(self.img, 1)

            cra = cv2.rectangle
            # cra(self.image, (start_x, start_y), (coor_x, coor_y),\
            # (255, 0, 0), 3)
            cra(self.image, (0, 0), (100, 100), (255, 0, 0), 3)
            # lineType(Int)
            # 8: 8連結（デフォルト値）
            # 4: 4連結
            # CV_AA: アンチエイリアス

            print "Select: " + str(self.coor_x) + ", " + str(self.coor_y)

            # # !!!: 2016/05/18 以下からできない！！！
            # is_drawable = True
            # while is_drawable is True:
            #     cv2.rectangle(image, (start_x, start_y), (coor_x, coor_y),\
            #             (255, 0, 0), 3)
            #     print "Select: " + str(coor_x) + ", " + str(coor_y)
            #     cv2.waitKey(33) > 0

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
