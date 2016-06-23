#-------------------------------------------------------------------------------
# Name:        Trim.py
# Purpose:     Trimming master image
#
# Author:      Kilo11
#
# Created:     03/12/2015
# Copyright:   (c) SkyDog 2015
# Licence:     SDS10002
#-------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding: utf-8 -*-
#def Trim():
# デフォルトの文字コード 変更
import sys
# sysモジュール リロード
reload(sys)
# デフォルトの文字コード 出力
sys.setdefaultencoding('utf-8')

# モジュールインポート
import time
import numpy as np
import cv2
import cv2.cv as cv
#------------------------------------------------------------

#マウスイベント関数 定義
def Mouse_trim(event,x,y,flags,param):
#グローバル変数 宣言
    global CapImage,\
        TrimAreaS,TrimAreaSx,TrimAreaSy,\
        TrimmingFlagS,TrimmingFlagC,\
        TrimAreaM1,TrimAreaM1x,TrimAreaM1y,\
        TrimmingFlagM,\
        TrimLen,TrimLenX,TrimLenY,\
        TrimEm,TrimEmx,TrimEmy,\
        TrimmingFlagE,\
        height,width,\
        TrimAreaM2,\
        TrimAreaE

#初回画像 表示
    cv2.imshow('Trim',CapImage)
#------------------------------

#左クリック押下で矩形描画 開始
#左クリック 押下毎に元画像を再読込して
#古い矩形を消去（2回め以降の描画用）
    if event == cv2.EVENT_LBUTTONDOWN:
        CapImage = cv2.imread('CapImage.png')
        cv2.imshow('Trim',CapImage)
#左クリックの座標 取得
        TrimAreaS = (x,y)
        TrimAreaSx = x
        TrimAreaSy = y
#座標位置 プロンプト出力
        print 'Start Trim: '+str(x)+', '+str(y)
#矩形選択開始フラグ OFF → ON
        TrimmingFlagS = False
        TrimmingFlagS = True
        TrimmingFlagC = True
        TrimmingFlagE = False
#------------------------------

#ドラッグで矩形 描画
    elif event == cv2.EVENT_MOUSEMOVE:
        if TrimmingFlagS == True and TrimmingFlagC == True:
#ドラッグの座標 取得
            TrimAreaM1 = (x, y)
            TrimAreaM1x = x
            TrimAreaM1y = y
#座標位置 プロンプト出力
            print 'Selected: '+str(x)+', '+str(y)
#マウスが移動したら（取得値が前回から変わったら）以下の処理
#上記処理を入れないと座標が'垂れ流し'状態になる
            if TrimAreaM1 != TrimAreaM2 and TrimmingFlagS == True:
                TrimmingFlagM = True
#前回の描画 消去
                CapImage = cv2.imread('CapImage.png')

        TrimLenX = abs(2 * TrimAreaSx - TrimAreaM1x)
        TrimLenY = abs(2 * TrimAreaSy - TrimAreaM1y)
        TrimLen = (TrimLenX,TrimLenY)

        cv2.rectangle(CapImage,TrimLen,TrimAreaM1,(255,255,255),2)
#マウス移動有無評価用最終値 取得
        TrimAreaM2 = (x, y)
#------------------------------

#左クリック押上で矩形描画 完了
    elif event == cv2.EVENT_LBUTTONUP:
        TrimmingFlagC = False
        if TrimmingFlagS == True and TrimmingFlagM == True:
            while True:
                TrimmingFlagE = False
#左クリック押上の座標 取得
                TrimAreaE = (x, y)
                TrimAreaEx = x
                TrimAreaEy = y
                print 'End Trim: '+str(x)+', '+str(y)

#          TrimEx = abs(2 * TrimAreaSx + TrimAreaEx)
#          TrimEy = abs(2 * TrimAreaSy + TrimAreaEy)
#          TrimE = (TrimEx,TrimEy)
#矩形描画 開始
                cv2.rectangle(CapImage,TrimLen,TrimAreaE,(255,0,0),1)

    #トリミングサイズ 導出
                width = abs(TrimAreaEx - TrimAreaSx) - 2
                height = abs(TrimAreaEy - TrimAreaSy) - 2
    #            width = (TrimAreaS[0] - TrimAreaE[0]) - 1
    #            height = (TrimAreaS[1] - TrimAreaE[1]) - 1
                TrimmingFlagS = False
                TrimmingFlagM = False
                TrimmingFlagE = True
#------------------------------------------------------------

#各変数初期値 代入
TrimmingFlagS = False
TrimmingFlagE = False
TrimMode = False
TrimAreaM2 = (0,0)
i = 1
TrimX = 0
TrimY = 0
height = 0
width = 0
#------------------------------------------------------------

#カメラ動画 取得
Capture = cv2.VideoCapture(0)
#動画取得エラー 処理
if Capture.isOpened() is False:
        raise('Can not get video')

#描画ウインドウ 作成
cv2.namedWindow('Capture', cv2.WINDOW_AUTOSIZE)

while True:
        Ret, Image = Capture.read()
        if Ret == False:
         continue
#------------------------------------------------------------

#動画操作方法 画面出力
        OpeFontLocU = (10,Image.shape[0] - 30)
        OpeFontLocL = (10,Image.shape[0] - 10)
        OpeFontScale = 0.7
        cv2.putText(Image,'Captcha mode:Long press t',OpeFontLocU,cv2.FONT_HERSHEY_SIMPLEX,OpeFontScale,(0,0,0),3)
        cv2.putText(Image,'Captcha mode:Long press t',OpeFontLocU,cv2.FONT_HERSHEY_SIMPLEX,OpeFontScale,(225,225,225),3 - 2)
        cv2.putText(Image,'Back:Long press Esc',OpeFontLocL,cv2.FONT_HERSHEY_SIMPLEX,OpeFontScale,(0,0,0),3)
        cv2.putText(Image,'Back:Long press Esc',OpeFontLocL,cv2.FONT_HERSHEY_SIMPLEX,OpeFontScale,(225,225,225),3 - 2)

#------------------------------------------------------------
        cv2.imshow('Capture', Image)

#tキー押下で動画から画像 取得
        if cv2.waitKey(50) == ord('t'):
            TrimMode = True
            cv2.imwrite('CapImage.png',Image)
            CapImage = cv2.imread('CapImage.png')
#------------------------------------------------------------

#トリム操作方法 画面出力
            OpeFontLocU = (10,20)
            OpeFontLocL = (10,CapImage.shape[0] - 10)
            OpeFontScale = 0.7
            cv2.putText(CapImage,'Select Area:Drag center Captcha:Long press S',OpeFontLocU,cv2.FONT_HERSHEY_SIMPLEX,OpeFontScale,(0,0,0),3)
            cv2.putText(CapImage,'Select Area:Drag center Captcha:Long press S',OpeFontLocU,cv2.FONT_HERSHEY_SIMPLEX,OpeFontScale,(225,225,225),3 - 2)
#         cv2.putText(CapImage,'Back:Long press Esc',OpeFontLocL,cv2.FONT_HERSHEY_SIMPLEX,OpeFontScale,(0,0,0),3)
#         cv2.putText(CapImage,'Back:Long press Esc',OpeFontLocL,cv2.FONT_HERSHEY_SIMPLEX,OpeFontScale,(225,225,225),3 - 2)

#------------------------------------------------------------
            cv2.imshow('Trim',CapImage)
            cv2.setMouseCallback('Trim',Mouse_trim)

#sキーが押されたら画像を保存
#上書き保存確認を追加！！！
        if cv2.waitKey(50) == ord('s') and TrimmingFlagE == True:
            TemplateSize = CapImage[TrimAreaSy - height:TrimAreaSy + height,\
                                 TrimAreaSx - width:TrimAreaSx + width]
            cv2.imwrite("template_%04d.png" % i,\
            TemplateSize)
#上書き保存確認ができるようになってからインクリメント処理を追加！！！
#         i += 1
            print("template_%04d.png" % i)
            TrimmingFlagS = False
            TrimmingFlagE = False
#前回の描画 消去
            CapImage = cv2.imread('CapImage.png')
            cv2.destroyWindow('Trim')
#------------------------------------------------------------

#Escキー押下 動画取得に戻る
        elif cv2.waitKey(50) & 0xFF == 27 and TrimMode == True:
            TrimMode = False
            cv2.destroyWindow('Trim')
#意図しない連続Esc対策 ディレイ
            time.sleep(1.0)

#Escキー押下 終了
        elif cv2.waitKey(50) & 0xFF == 27 and TrimMode == False:
            break

#Capture.release()
cv2.destroyWindow('Capture')
