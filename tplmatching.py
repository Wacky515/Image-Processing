# !/usr/bin/python
# vim: set fileencoding = utf-8:  # デフォルトの文字コード 変更
# --------------------------------------------------# {{{
# file_name:   tplmatching
# Purpose:     TemplateMatching
#
# Author:      Kilo11
#
# Created:     23/03/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10001.200
# --------------------------------------------------
u""" テンプレートマッチングによる画像処理 """
# }}}

# TODO: Python3系 対応！！！
# TODO: 関数名は動詞にする
# TODO: 変数は "[大区分]_[小区分]"
# TODO: Unicode文字リテラルを " u"body" " -> " "body" " に変更
# DONE: 文字列の埋込を % 形式から format 形式に変更
# DONE: "print" -> "print()" に変更

# モジュール インポート# {{{
import numpy as np
import os
# import glob
import time
# import unittest
import pdb; pdb.set_trace()

import cv2
# import cv2.cv as cv

import trim as tm

import sys
sys.path.append("D:\OneDrive\Biz\Python\SaveDate")

import savedata as sd

# sysモジュール リロード
reload(sys)

# デフォルトの文字コード 出力
sys.setdefaultencoding("utf-8")
# }}}


def terminate(name_cap=0, time_wait=33):
    u""" 出力画像 終了処理 """# {{{
    # name_cap: 0: 静止画 1: 動画
    cv2.waitKey(time_wait)
    if name_cap != 0:
        name_cap.release
    cv2.destroyAllWindows()
    print("Terminated...")
    sys.exit()
# }}}


class GetImage:
    u""" 画像・動画 取得クラス """
    def __init__(self, image):
        self.image = image

    def get_image(self, conversion=1):
        u""" 画像・動画 読込み """
        try:
            image = cv2.imread(self.image, conversion)
            return image
        # 画像取得 エラー処理
        except:
            print ("Image data is not found...")
            return False

    def display(self, name_window, image, _type=1):
        u""" 画像・動画 画面出力 """
        # _type: 0: 静止画 1: 動画 切換え
        # 静止画無し判定時 処理 ← "is None" にした 動作確認！！！
        if image is None and _type == 0:
            print ("Getting image...")
            image = self.get_image()
        print ("Display {}s...".format(name_window))
        cv2.namedWindow(name_window, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(name_window, image)
        print (u"画像の大きさを取得する処理を実装！！！")
        if _type == 0:
            # 静止画の出力保持処理
            terminate(0, 0)


class ConvertImage(GetImage):
    u""" 画像・動画 変換クラス """  # {{{
    def __init__(self):
        pass

    def grayscale(self, image):
        u""" グレースケール 変換処理 """
        print ("Convert grayscale...")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    def adaptive_threashold(self, image):
        u""" 適応的二値化 変換処理 """
        gray = self.grayscale(image)
        # 適応的二値化(Adaptive Gaussian Thresholding) パラメタ定義# {{{
        # *** 適応的二値化 解説 ***
        # 1画素枚に、任意の近傍画素から個別の閾値を算出
        # *** 以上 ***
        # }}} """
        # 最大閾値
        thresh_max = 255
        # 閾値算出アルゴリズム# {{{
        # GaussianC:任意の近傍画素をGaussianによる重付け（近傍を重視）で総和し
        # 閾値を算出
        # MeanC:任意の近傍画素を算術平均し閾値を算出
        # }}} """
        algo = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        # algo = cv2.ADAPTIVE_THRESH_MEAN_C
# 閾値処理
        thresh_type = cv2.THRESH_BINARY
        # thresh_type = cv2.THRESH_BINARY_INV
        # 切取る正方形の一の画素数（3、5、7... 奇数のみ！）
        area_calc = 7
        # 減算定数# {{{
        #   周囲が似た色の時、減算して閾値を意図的に突出させ
        #   背景領域のノイズ・色ゆらぎの影響を低減する
        # }}}
        subtract = 4
        # 適応的二値化 変換処理
        print ("Convert adaptive threashold...")
        cat = cv2.adaptiveThreshold
        adpth = cat(gray, thresh_max, algo, thresh_type, area_calc, subtract)
        return adpth

    def bilateral_filter(self, image):
        u""" バイラテラルフィルタ 処理 """
        gray = self.grayscale(image)
        # 切取る正方形の一の画素数（3、5、7... 奇数のみ！）
        # 数値が大きいほどぼやける
        area_calc = 7
        # 色空間におけるフィルタシグマ      大きくなると色の領域がより大きくなる
        color_sigma = 12
        # 座標空間におけるフィルタシグマ    大きくなるとより遠くの画素同士が影響する
        metric_sigma = 3
        print ("Bilateral filtering...")
        cvf = cv2.bilateralFilter
        blr = cvf(gray, area_calc, color_sigma, metric_sigma)
        return blr

    def discriminantanalyse(self, image):
        u""" 判別分析法 処理 """
        image = self.bilateral_filter(image)
        thresh_std = 40
        thresh_max = 255
        method = cv2.THRESH_BINARY + cv2.THRESH_OTSU
        print ("Discriminant analysing...")
        cth = cv2.threshold
        ret, dcta = cth(image, thresh_std, thresh_max, method)
        return dcta

    def binarize(self, image):
        u""" 二値化 処理 """
        image = self.bilateral_filter(image)
        thresh_std = 70
        thresh_max = 255
        method = cv2.THRESH_BINARY_INV
        print ("Binarizing...")
        cth = cv2.threshold
        ret, binz = cth(image, thresh_std, thresh_max, method)
        return binz

    def normalize(self, image):
        u""" 正規化 処理 """
        # alpha、beta 解説（わからん！！！）# {{{
        # alpha:ノルム正規化の場合、正規化されるノルム値。範囲正規化の場合、下界
        # beta:ノルム正規化の場合、不使用。範囲正規化の場合、の上界
        # }}}
        alpha = 0
        beta = 1
        algo = cv2.NORM_MINMAX
        print ("Normalizing...")
        norm = cv2.normalize(image, alpha, beta, algo)
        return norm
# }}}


class Tplmatching:
    u""" テンプレートマッチング クラス """
    def __init__(self):
        pass

    def tplmatch(self, image, tpl):
        u""" テンプレートマッチング 処理 """
        # 類似判定アルゴリズム 解説# {{{
        # CV_TM_SQDIFF    :輝度値の差の２乗の合計     小さいほど類似
        # CV_TM_CCORR     :輝度値の相関               大きいほど類似
        # CV_TM_CCOEFF    :輝度値の平均を引いた相関   大きいほど類似
        #                 （テンプレート画像と探索画像の明るさに左右されにくい）
        # }}} """
        algo = cv2.TM_CCOEFF_NORMED
        match = cv2.matchTemplate(image, tpl, algo)
        # 類似度の最小・最大値と各座標 取得
        value_min, value_max, loc_min, loc_max = cv2.minMaxLoc(match)
        return match, value_min, value_max, loc_min, loc_max


class ImageProcessing:
    u""" 動画取得 クラス """
    def __init__(self):
        self.ci = ConvertImage()
        self.tm = Tplmatching()
        # 動画 取得
        self.cap = cv2.VideoCapture(0)

    def init_get_camera_image(self, name):
        u""" カメラから動画取得 """
        # カメラキャプチャ時のイニシャライズ ディレイ処理
        time.sleep(0.1)
        if not self.cap.isOpened():
            print ("Can not connect camera...")
            terminate()
            # トラックバー 定義(できない)！！！# {{{
            #        name_bar = "Max threshold"
            #        print (thresh_max)
            # # トラックバー 生成
            #        def set_parameter(value):
            #            thresh_max = cv2.getTrackbarPos(name_bar, name_window)
            #            thresh_max = cv2.setTrackbarPos(name_bar, name_window)
            #        cv2.createTrackbar(name_bar, name_window,
            #           0, 255, self.thresh_max)
            #        name_window = "Adaptive Threashold cap"
            # }}}
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

    def run(self, name, search, extension=".png", dir_master="MasterImage"):
        u""" 動画取得 処理（メインルーチン） """  # {{{
        print ("-------------------------------------------------")
        print ("Start template matching")
        print ("-------------------------------------------------")
        print ("\t*** Search master mode ***\r\n")
        cwd = os.getcwd()
        path_master = cwd + "\\" + dir_master
        print ("Master directory: \r\n\t" + path_master)

        # マスター画像 検索
        sda = sd.SaveData(search, path_master)
        set_name, name_master, match_flag = sda.get_name_max(extension)
        print ("\t*** Return search master mode ***\r\n")

        # マスター画像有無 判定
        if match_flag is False:
            print ("No match master")
            print ("Go get master mode(no match master case)\r\n")
            self.get_master(search, extension, path_master)
            set_name, name_master, match_flag = sda.get_name_max(extension)
            print ("Get master name: " + str(name_master))
        else:
            print ("Match master name: " + str(name_master))
            print ("Match master extension: " + str(extension))

        self.init_get_camera_image(name)

        # !!!: ここから
        count = 0
        while True:
            if count < 1:
                print ("Initial delay")
                time.sleep(0.1)
            get_flag, frame = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            # TODO: 操作説明 表示！！！
            cv2.imshow(name, frame)
            print ("Capture is running...")
            count += 1
        # !!!: 以上までをclassにしたいが"while"内の"frame"を
        # "while"外に出せないので断念！！！
        # ↑関数にする(できなかった！！！)？？？
            # }}}

            # 動画 変換・画像処理（まとめる）！！！# {{{
            adpth = self.ci.adaptive_threashold(frame)
            self.ci.display("Adaptive threashold", adpth, 1)
            dcta = self.ci.discriminantanalyse(frame)
            self.ci.display("Discriminant analyse", dcta, 1)
            binz = self.ci.binarize(frame)
            self.ci.display("Bilateral filter", binz, 1)
# }}}

            # テンプレートマッチング 処理
            print("\r\nMaster name: " + str(name_master) + str(extension) + "\r\n")
            master = str(path_master) + ".\\"\
                    + str(name_master) + str(extension)
            master = cv2.imread(str(master), cv2.IMREAD_COLOR)
            self.ci.display("Master", master)

            match, value_min, value_max, loc_min, loc_max \
                    = self.tm.tplmatch(frame, master)
            print (value_max)

            # 2016/06/03 ここまで！！！
            # "t"キー押下 マスター画像取得モード 遷移
            if cv2.waitKey(33) == ord("t"):
                print "\r\nInput key \"t\""
                print("Go get master mode\r\r\n")
                time.sleep(1)
                self.get_master(search, extension, path_master)
                set_name, name_master, match_flag = sda.get_name_max(extension)
                print ("Get master name: " + str(name_master))
                # img = "master_source{}".format(extension)
                # cv2.imwrite(img, frame)
                # trim = tm.Trim(img, search, extension, path_master)
                # trim.trim()

            # 仮の終了処理！！！
            # "q"キー押下 終了処理
            if cv2.waitKey(33) == ord("e"):
                print "\r\nInput key \"e\""
                time.sleep(1)
                print ("*** End process ***\t\r\n")
                break
            # if cv2.waitKey(33) > 0:
            #     break
            #     # terminate(cap)


    def get_master(self, search, extension, path):
        u""" マスター画像 読込み """
        print ("*** Start get master mode ***\t")
        print ("Search master name: " + str(search))
        name = "Get master image"
        text2 = "Quit: Long press \"q\" key"
        text3 = "Trim mode: Long press \"t\" key"

        print ("Master image name: " + str(search))

        self.init_get_camera_image(name)

        count = 0
        while True:
            if count < 1:
                print ("Initial delay")
                time.sleep(0.1)
            get_flag, frame = self.cap.read()
            get_flag_draw, frame_draw = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            # 操作方法説明文 表示位置 取得
            text_offset = 10
            baseline = frame.shape[0] - text_offset
            origin = 1, baseline

            # 操作方法説明文 表示
            trim = tm.Trim(frame_draw, search, extension, path, 1)
            text_height = trim.write_text(text2, origin)
            trim.write_text(text3,\
                    (origin[0], origin[1] - text_offset - text_height[1]))

            cv2.imshow(name, frame_draw)
            print ("Master captcha")
            count += 1

            # "t"キー押下 マスター画像取得モード 遷移
            if cv2.waitKey(33) == ord("t"):
                print "\r\nInput key \"t\""
                print("Go master mode")
                time.sleep(1)
                img = "master_source{}".format(extension)
                cv2.imwrite(img, frame)
                trim = tm.Trim(img, search, extension, path)
                trim.trim()

            # "q"キー押下 終了処理
            if cv2.waitKey(33) == ord("q"):
                print "\r\nInput key \"q\""
                time.sleep(1)
                print ("*** End get master mode ***\t\r\n")
                break

    def check_get_flag(self, flag):
        u""" 動画取得ミス時 スキップ処理 """  # {{{
        if flag is False:
            print ("Can not get end flag")
            return False
            # }}}

    def check_get_frame(self, frame):
        u""" ループ 終了処理 """  # {{{
        if frame is None:
            print ("Can not get video frame")
            return False
            # }}}


def main():
    # vimテスト用各変数 定義# {{{
    # テスト出力
    print ("\r\n--------------------------------------------------")
    print ("Information")
    print ("--------------------------------------------------")
    print ("Default current directory is...")
    print ("\t" + os.getcwd())
    print ("\r\nAnd then...")
    os.chdir("D:\OneDrive\Biz\Python\ImageProcessing")
    print ("\t" + os.getcwd())
    print (u"\r\n〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓")
    print ("Start main")
    print (u"〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓")

    path = "D:\\OneDrive\\Biz\\Python\\ImageProcessing"
    smpl_pic = "D:\\OneDrive\\Biz\\Python\\ImageProcessing\\tpl_1.png"
    smpl_pic2 = "D:\\OneDrive\\Biz\\Python\\ImageProcessing\\tpl_2.png"
# }}}

    # テンプレートマッチング テスト# {{{
    cip = ImageProcessing()
    cip.run("Raw capture", "masterImage")
    # print ("Movie captcha end...")
    # }}}

#     # 静止画取得 テスト# {{{
#     gim = GetImage(smpl_pic)
#     gim2 = GetImage("tpl_3.png")
#     # gim.diplay("Tes1", 0, 0)
#     gim2.display("Tes2", 0, 0)
#     print ("Main loop end...")
# # }}}

# # 動画取得 テスト# {{{
#     cav = CapVideo()
#     cav.get_video("Capture_test")
#     frame_test = cav.frame
#     if frame_test is None:
#         gm = GetImage(smpl_pic)
#         gm.get_image()
#     name = "Test"
#     Image = cv2.imread(smpl_pic2)
#     cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
#     cv2.imshow(name, Image)
#     cv2.imshow(name, frame_test)
#     # 仮の出力保持処理！！！
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#     image = cv2.imread("tpl_2.png")
#     ci = ConvertImage()
#     ci.adaptive_threashold(image, "Adaptive Threashold", 0)
#     print ("Sudah cap")
# # }}}

    # # ドキュメントストリング# {{{
    # print (GetImage.__doc__)
    # print (help(__name__))
    # }}}

if __name__ == '__main__':
    main()

#    unittest.main()
