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
# Gdiff test

# モジュール インポート
import numpy as np
import cv2
import cv2.cv as cv
import os
import tplmatching as tpm
import getch

import sys
# sysモジュール リロード
reload(sys)

# デフォルトの文字コード 出力
sys.setdefaultencoding("utf-8")


class Trim(tpm.GetImage):
    u""" トリミング クラス """
    def __init__(self):
        pass

    def start_trim(self, image):
        u""" トリミング 開始 """
        gim = tpm.GetImage(image)
        gim.display("Original image")
        key = ord(getch.getch())
        event = 0
        coor_x = 0
        coor_y = 0
        if event == cv2.EVENT_LBUTTONDOWN:
            # 古い矩形を消去（2回目以降の描画用） 一旦キル！！！
            # cv2.imshow("Original image", image)
            # while(event > 0):
            print "Selected positon:" + str(coor_x) + ", " + str(coor_y)
            if(key == 3):  # key 3:"Ctrl + c"
                print("Quit")
                # break

        tpm.termination(0, 0)

        # if event == cv2.EVENT_LBUTTONDOWN:
# 左クリック押下 画像再描画（いらない表示を消す＝文字のない画像を受け取る！！）
        # image = cv2.imread("***.png")


def main():
    u""" メインルーチン """
    print os.getcwd()
    os.chdir("D:\\OneDrive\\Biz\\Python\\TemplateMatching")
    print os.getcwd()

    tm = Trim()
    tm.start_trim("trim_test.png")

if __name__ == '__main__':
    main()
