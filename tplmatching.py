# !/usr/bin/python
# -*- coding: utf-8 -*-
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
# }}}
""" テンプレートマッチングによる画像処理 """

# TODO: 変数は "[大区分/固有]_[小区分/汎用]"

# TODO: OCR 実装
# TODO: GUI 実装
# TODO: 画像出力ウィンドウの位置を定義（固定）する
# TODO: 複数索敵・多段式判定を実装する
#       -> インスタンスをイテレートする？
# TODO: 色識別 実装
# TODO: 関数名は動詞にする

# {{{
# DONE: "matchTemplate" の "TM_CCOEFF_NORMED" は正規化する必要があるのか調査
#       "***_NORMED"以外は正規化している
# DONE: Python3系 対応！！！
# DONE: Unicode文字リテラルを " u"body" " -> " "body" " に変更
# DONE: 文字列の埋込を % 形式から format 形式に変更
# DONE: "print" -> "print()" に変更
# ABORT: ワークを動体検出後に判定開始する
# ABORT: ワーク検出は背景差分で行う
# }}}

# モジュール インポート# {{{
import numpy as np
import os
# import glob
import time
# import unittest

import cv2
# import cv2.cv as cv

import trim as tm

import sys
sys.path.append("D:\OneDrive\Biz\Python\SaveDate")
sys.path.append("D:\OneDrive\Biz\Python\Sound")

import savedata as sd
import judgesound as js

# sysモジュール リロード
reload(sys)

# デフォルトの文字コード 出力
sys.setdefaultencoding("utf-8")
# }}}

print_col = 50
save_lim = 2


def terminate(name_cap=0, time_wait=33):
    """ 出力画像 終了処理 """  # {{{
    # name_cap: 0: 静止画 1: 動画
    cv2.waitKey(time_wait)
    if name_cap != 0:
        name_cap.release
    cv2.destroyAllWindows()
    print("Terminated...")
    sys.exit()
# }}}


class GetImage:
    """ 画像・動画 取得クラス """  # {{{
    def __init__(self, image):
        self.image = image

    def get_image(self, conversion=1):
        """ 画像・動画 読込み """
        try:
            image = cv2.imread(self.image, conversion)
            return image
        # 画像取得 エラー処理
        except:
            print("Image data is not found...")
            return False

    def display(self, window_name, image, _type=1):
        """ 画像・動画 画面出力 """
        # _type: 0: 静止画 1: 動画 切換え
        # 静止画無し判定時 処理 ← "is None" にした 動作確認！！！
        if image is None and _type == 0:
            print("Getting image...")
            image = self.get_image()
        print("Display {}s...".format(window_name))
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_name, image)
        if _type == 0:
            # 静止画の出力保持処理
            terminate(0, 0)
# }}}


class ConvertImage(GetImage):
    """ 画像・動画 変換クラス """  # {{{
    # 閾値処理 手法リスト
    THRESH_METHODS = ["cv2.THRESH_BINARY",
                        "cv2.THRESH_BINARY_INV",
                        "cv2.THRESH_TRUNC",
                        "cv2.THRESH_TOZERO",
                        "cv2.THRESH_TOZERO_INV",
                        "cv2.THRESH_BINARY + cv2.THRESH_OTSU",
                        "cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU",
                        "cv2.THRESH_TRUNC + cv2.THRESH_OTSU",
                        "cv2.THRESH_TOZERO + cv2.kHRESH_OTSU",
                        "cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU"]

    def __init__(self):
        pass

    def grayscale(self, image):
        """ グレースケール 変換処理 """
        print("Convert grayscale...")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    def adaptive_threashold(self, image, algo=1, method=0):
        """ 適応的二値化 変換処理 """
        gray = self.grayscale(image)
        # 適応的二値化(Adaptive Gaussian Thresholding) パラメタ定義# {{{
        # *** 適応的二値化 解説 ***
        # 1画素枚に、任意の近傍画素から個別の閾値を算出
        # }}}
        # 最大閾値
        THRESH_MAX = 255
        # 閾値算出アルゴリズム# {{{
        # MeanC:        任意の近傍画素を算術平均し閾値を算出
        # GaussianC:    任意の近傍画素をGaussianによる重み付け
        #               （近傍を重視）で総和し閾値を算出
        # }}} """
        THRESH_ALGOS = ["cv2.ADAPTIVE_THRESH_MEAN_C",
                        "cv2.ADAPTIVE_THRESH_GAUSSIAN_C"]
        # 切取る正方形の一の画素数（3、5、7... 奇数のみ！）
        area_calc = 7
        # 減算定数# {{{
        #   周囲が似た色の時、減算して閾値を意図的に突出させ
        #   背景領域のノイズ・色ゆらぎの影響を低減する
        # }}}
        subtract = 4
        # 適応的二値化 変換処理
        print("Convert adaptive threashold...")
        cat = cv2.adaptiveThreshold
        adpth = cat(gray, THRESH_MAX, eval(THRESH_ALGOS[algo]),
                    eval(self.THRESH_METHODS[method]), area_calc, subtract)
        # adpth = cat(gray, THRESH_MAX, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    # cv2.THRESH_BINARY, area_calc, subtract)
        return adpth

    def bilateral_filter(self, image):
        """ バイラテラルフィルタ 処理 """
        gray = self.grayscale(image)
        # 切取る正方形の一の画素数（3、5、7... 奇数のみ！）
        #   数値が大きいほどぼやける
        area_calc = 7
        # 色空間におけるフィルタシグマ
        #   大きくなると色の領域がより大きくなる
        color_sigma = 12
        # 座標空間におけるフィルタシグマ
        #   大きくなるとより遠くの画素同士が影響する
        metric_sigma = 3
        print("Bilateral filtering...")
        cvf = cv2.bilateralFilter
        blr = cvf(gray, area_calc, color_sigma, metric_sigma)
        return blr

    def discriminantanalyse(self, image,
                            thresh_std=128, method=5):
        """ 判別分析法 処理 """
        image = self.bilateral_filter(image)
        print("Discriminant analysing...")
        cth = cv2.threshold
        # 最大閾値
        THRESH_MAX = 255
        ret, dcta = cth(image, thresh_std,
                        THRESH_MAX, eval(self.THRESH_METHODS[method]))
        return dcta

    def binarize(self, image, thresh_std=128, method=1):
        """ 二値化 処理 """
        image = self.bilateral_filter(image)
        print("Binarizing...")
        cth = cv2.threshold
        # 最大閾値
        THRESH_MAX = 255
        ret, binz = cth(image, thresh_std,
                        THRESH_MAX, eval(self.THRESH_METHODS[method]))
        return binz

    def normalize(self, image, alpha=0, beta=1):
        """ ノルム正規化 処理 """
        # alpha、beta 解説# {{{
        # TODO: わからんから図書館で資料を借りる！！！
        # TODO: 特にアルファ、ベータの数値の意味合いと妥当性！！！
        # alpha:ノルム正規化の場合、正規化されるノルム値
        #        範囲正規化の場合、下界
        # beta:ノルム正規化の場合、不使用
        #        範囲正規化の場合、の上界
        # }}}
        algo = cv2.NORM_MINMAX
        print("Normalizing...")
        norm = cv2.normalize(image, image, alpha, beta, algo)
        return norm
# }}}


class Tplmatching:
    """ テンプレートマッチング クラス """
    def __init__(self):
        self.cim = ConvertImage()

    def tplmatch(self, image, tpl, algo=5):
        """ テンプレートマッチング 処理 """
        # 類似度判定アルゴリズム 解説# {{{
        # cv2.TM_SQDIFF    :輝度値の差の２乗の合計     小さいほど類似
        # cv2.TM_CCORR     :輝度値の相関               大きいほど類似
        # cv2.TM_CCOEFF    :輝度値の平均を引いた相関   大きいほど類似
        #                 （テンプレート画像と探索画像の明るさに左右されにくい）
        # cv2.TM_***_NORMED :上記それぞれの正規化版
        # }}} """
        ALGOS = ["cv2.TM_SQDIFF",
                    "cv2.TM_SQDIFF_NORMED",
                    "cv2.TM_CCORR",
                    "cv2.TM_CCORR_NORMED",
                    "cv2.TM_CCOEFF",
                    "cv2.TM_CCOEFF_NORMED"]
        match = cv2.matchTemplate(image, tpl, eval(ALGOS[algo]))
        if ALGOS in ["cv2.TM_SQDIFF", "cv2.TM_CCORR", "cv2.TM_CCOEFF"]:
            # ノルム正規化 処理
            norm = self.cim.normalize(match)
            # 類似度の最小・最大値と各座標 取得
            value_min, value_max, loc_min, loc_max = cv2.minMaxLoc(norm)
        else:
            value_min, value_max, loc_min, loc_max = cv2.minMaxLoc(match)
        return match, value_min, value_max, loc_min, loc_max

    def mask(self):
        """ マスク 処理（将来的に実装） """
        # 初回でマッチした近傍領域以外にマスク処理し、処理速度向上する
        # ただし索敵位置が動的に変化しない前提
        pass

    def calc_detect_location(self, loc_max, master, location="center"):
        """ 補足座標 演算 """
        height, width, channel = master.shape
        # 中央座標 演算
        if location == "center":
            coord = (loc_max[0] + width / 2, loc_max[1] + height / 2)
        # 右下座標 演算
        elif location == "tail":
            coord = (loc_max[0] + width, loc_max[1] + height)
        return coord, height, width

    def show_detect_area(self, loc_max, frame, master):
        """ 補足範囲 演算 """
        # 中央座標 演算
        coord, height, width\
            = self.calc_detect_location(loc_max, master, "center")
        left_up = (loc_max[0], loc_max[1])
        right_bottom = (loc_max[0] + width, loc_max[1] + height)
        detect = frame[loc_max[1]:loc_max[1] + height,
                        loc_max[0]:loc_max[0] + width].copy()
        return detect, left_up, right_bottom


class ImageProcessing:
    """ 動画取得 クラス """
    def __init__(self):

        self.cim = ConvertImage()
        self.tmc = Tplmatching()
        self.jsd = js.JudgeSound()

        self.ciadp = self.cim.adaptive_threashold
        self.cidca = self.cim.discriminantanalyse
        self.cibiz = self.cim.binarize
        self.cinor = self.cim.normalize

        # 動画 取得
        self.cap = cv2.VideoCapture(0)
        self.text3 = "Mastering: Long press \"m\" key"

        # マッチ判定値
        self.judge_detect = 0.30
        self.judge_ok = 0.70
        # OK/NG 表示固定flag
        self.judge_flag = True

        # OKと判定する時間
        self.ok_time = 2
        self.ok_count = 0

        # Beep音 再生回数固定用 カウンタ
        self.beep_count = 0

        # 正規化（強調表示）の強調度
        self.highlight = 4

        # 操作説明文
        self.text2 = "End: Long press \"e\" key"

    def get_camera_image_init(self, name, gen_window=0):
        """ カメラから動画取得 """
        # カメラキャプチャ時のイニシャライズ ディレイ処理
        time.sleep(0.1)
        if not self.cap.isOpened():
            print("Can not connect camera...")
            terminate()
            # トラックバー 定義(できない)！！！# {{{
            #        bar_name = "Max threshold"
            #        print(thresh_max)
            # # トラックバー 生成
            #        def set_parameter(value):
            #            thresh_max = cv2.getTrackbarPos(bar_name, window_name)
            #            thresh_max = cv2.setTrackbarPos(bar_name, window_name)
            #        cv2.createTrackbar(bar_name, window_name,
            #           0, 255, self.thresh_max)
            #        window_name = "Adaptive Threashold cap"
            # }}}
        if gen_window != 0:
            cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

    def run(self, name, search, extension=".png",
            dir_master="MasterImage", dir_judge="LogImage"):
        """ 動画取得 処理（メインルーチン） """  # {{{
        print("-" * print_col)
        print("START TEMPLATE MATCHING".center(print_col, " "))
        print("-" * print_col)
        print("")
        print(" SEARCH MASTER MODE ".center(print_col, "*"))
        print("")
        cwd = os.getcwd()
        path_master = cwd + "\\" + dir_master
        print("Master directory:")
        print(path_master.rjust(print_col, " "))

        # 最終枝番のマスター画像 取得
        # TODO: 複数探査の時はここの" sda "をイテレート処理！！！
        sda = sd.SaveData(search, path_master)
        set_name, master_name, match_flag = sda.get_name_max(extension)

        print(" RETURN TEMPLATE MATCHING ".center(print_col, "*"))
        print("")

        # マスター画像有無 判定
        if match_flag is False:
            print("No match master")
            print("Go get master mode(None master case)")

            # マスター画像取得モード 遷移
            while match_flag is False:
                self.get_master(search, extension, path_master, 1)
                set_name, master_name, match_flag = sda.get_name_max(extension)

            print("Get master name: " + str(master_name))
            print("")

        else:
            print("Match master name: " + str(master_name))
            print("Match master extension: " + str(extension))
            print("")
        # TODO: イテレート処理予定 ここまで！！！

        self.get_camera_image_init(name)

        # !!!: ここから
        count = 0
        while True:
            if count == 0:
                print("Initial delay")
                time.sleep(0.1)
            get_flag, frame = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            print("Capture is running...")
            count += 1
            # import pdb; pdb.set_trace()
        # !!!: 以上までをclassにしたいが"while"内の"frame"を
        # "while"外に出せないので断念！！！
            # }}}

            # マスター画像の検索とセット 表示
            print("")
            print("Master name: "\
                    + str(master_name) + str(extension) + "\r\n")

            master = str(path_master) + ".\\"\
                    + str(master_name) + str(extension)
            master = cv2.imread(str(master), 1)

            # テンプレートマッチング イテレート処理
            # TODO: 複数探査の時はここのタプルにマスターを入れる
            # 評価用 処理リスト
            methods = [
                    ["Row", None],
                    # ["Adaptive threashold", self.ciadp],
                    # ["Discriminant analyse", self.cidca],
                    # ["Bilateral filter", self.cibiz]
                    ]

            for method in methods:
                if method[1] is not None:
                    frame_eval = method[1](frame)
                    master_eval = method[1](master)
                else:
                    frame_eval = frame
                    master_eval = master

                # テンプレートマッチング 処理
                match, value_min, value_max, loc_min, loc_max\
                        = self.tmc.tplmatch(frame_eval, master_eval)

                # 補足範囲 正規化（補足強調表示用）
                norm = self.cinor(match)

                # マッチ領域 トリム処理
                detect, left_up, right_bottom\
                        = self.tmc.show_detect_area(loc_max, frame, master)
                if method[1] is not None:
                    detect = method[1](detect)

                # マッチ 判定
                trim = tm.Trim(frame_eval, None, None, None, 1)

                # ワーク 検出処理
                if value_max > self.judge_detect:
                    msg_heigh, msg_base\
                            = trim.write_text("Matching...",
                            (0, "height"), offset=(0, 5))
                    judge_origin = (0, 15 + msg_base)
                    # *秒間OKで画面表示！！！
                    self.ok_count += 1
                    if self.ok_count == 1:
                        self.ok_start = time.time()
                        print("")
                        print("Start OK time: " + str(self.ok_start))
                        print("")
                    else:
                        wait_ok = time.time() - self.ok_start
                        print("")
                        print("OK frame count: " + str(self.ok_count))
                        print("Start OK time: " + str(self.ok_start))
                        print("OK time: " + str(round(wait_ok, 2)) + "[sec]")
                        print("")
                        if wait_ok > self.ok_time:

                            # OK/NG 判定処理
                            if value_max > self.judge_ok and\
                                    self.judge_flag is True:
                                self.beep_count += 1
                                # OK 表示
                                trim.write_text("OK", (0, "height"), 2,
                                                "white", "green",
                                                5, 4, judge_origin)
                                # 検出位置 矩形表示
                                trim.draw_rectangle(left_up, right_bottom,
                                                    "white", "green")
                                # 類似度 表示
                                similarity = round(value_max * 100, 1)
                                trim.write_text(str(similarity) + "%",
                                                (right_bottom[0], "height"),
                                                scale=0.6,
                                                color_out="white",
                                                color_in="green",
                                                thickness_out=3,
                                                thickness_in=2,
                                                offset=(0, right_bottom[1] + 5))

                                # OK音 出力
                                if self.beep_count == 2:
                                    self.jsd.beep_ok()

                                    # TODO: ログ 出力！！！
                                    # TODO: 保存画像は数を制限する
                                    sda_ok = sd.SaveData("ok_image", dir_judge)
                                    sda_ok.save_image(frame_eval, extension, mode=3)

                            else:
                                self.beep_count += 1
                                # NG 表示
                                self.judge_flag = False
                                trim.write_text("NG", (0, "height"), 2,
                                                "white", "red",
                                                5, 4, judge_origin)

                                # NG音 出力
                                if self.beep_count == 2:
                                    self.jsd.beep_ng()

                                # TODO: ログ 出力！！！

                # 検索中 表示
                if value_max < self.judge_detect:
                    trim.write_text("Searching...",
                                    (0, "height"), offset=(0, 5))
                    self.ok_count = 0
                    self.ok_start = 0
                    self.beep_count = 0
                    self.judge_flag = True

                # 評価処理 画面表示
                # self.cim.display(str(method[0] + " frame"), frame_eval)
                self.cim.display(str(method[0] + " master"), master_eval)
                self.cim.display("Detected " + str(method[0]), detect, 1)
                self.cim.display("Normalize " + str(method[0]),
                                norm ** self.highlight, 1)  # frameよりmaster分縮む

                # 操作方法説明文 表示位置 取得
                text_offset = 10
                baseline = frame.shape[0] - text_offset
                origin = 1, baseline

                # 操作方法説明文 表示
                operation = frame
                trim = tm.Trim(operation, None, None, None, 1)
                text_height = trim.write_text(self.text2, origin)
                trim.write_text(self.text3,\
                        (origin[0], origin[1] - text_offset - text_height[1]))

                # メイン画面 表示
                self.cim.display(name, operation)
                # import pdb; pdb.set_trace()

                # 結果 出力
                simil_max = str(round(value_max * 100, 2)) + "%"
                simil_min = str(round(value_min * 100, 2)) + "%"
                print("")
                print("{}".format(method[0]))
                print("Max similarity:")
                print(str(simil_max.rjust(print_col, " ")))
                print(str(loc_max).rjust(print_col, " "))
                print("Min similarity:")
                print(str(simil_min.rjust(print_col, " ")))
                print(str(loc_min).rjust(print_col, " "))

            # "m"キー押下 マスター画像取得モード 遷移
            if cv2.waitKey(33) == ord("m"):
                print("")
                print("Input key \"m\"")
                print("Go get master mode")
                print("")
                time.sleep(0.5)
                # TODO: 複数探査の時はここの" sda "をイテレート処理！！！
                self.get_master(search, extension, path_master, 1)
                set_name, master_name, match_flag = sda.get_name_max(extension)
                # TODO: イテレート処理予定 ここまで！！！
                cv2.destroyAllWindows()
                print("Get master name: " + str(master_name))

            # "e"キー押下 終了処理
            if cv2.waitKey(33) == ord("e"):
                print("")
                print("Input key \"e\"")
                print("")
                print(" END PROCESS ".center(print_col, "*"))
                print("")
                break

    def get_master(self, search, extension, path, mode=0):
        """ マスター画像 読込み """  # {{{
        self.search = search
        self.extension = extension
        self.path = path

        name = "Get master image"
        text2 = "Quit: Long press \"q\" key"
        text3 = "Trimming: Long press \"t\" key"

        print("")
        print(" START GET MASTER MODE ".center(print_col, "*"))
        print("Search master name: " + str(search))
        print("Master image name: " + str(search))

        self.get_camera_image_init(name)

        count = 0
        while True:
            if count == 0:
                print("Initial delay")
                time.sleep(0.1)
            get_flag, frame = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            # マスター画像取得モード 直接遷移
            if mode != 0:
                self.go_get_master_mode()
                break

            # 操作方法説明文 表示位置 取得
            text_offset = 10
            baseline = frame.shape[0] - text_offset
            origin = 1, baseline

            # 操作方法説明文 表示
            frame_draw = frame
            trim = tm.Trim(frame_draw, search, extension, path, 1)
            text_height = trim.write_text(text2, origin)
            trim.write_text(text3,\
                    (origin[0], origin[1] - text_offset - text_height[1]))

            self.cim.display(name, frame_draw)
            print("Master captcha")
            count += 1

            # "t"キー押下 マスター画像取得モード 遷移
            if cv2.waitKey(33) == ord("t"):
                self.go_get_mastner_mode()

            # "q"キー押下 終了処理
            if cv2.waitKey(33) == ord("q"):
                print("")
                print("Input key \"q\"")
                time.sleep(0.5)
                print(" END GET MASTER MODE ".center(print_col, "*"))
                print("")
                # import pdb; pdb.set_trace()
                break
# }}}

    def check_get_flag(self, flag):
        """ 動画取得ミス時 スキップ処理 """  # {{{
        if flag is False:
            print("Can not get end flag")
            return False
            # }}}

    def check_get_frame(self, frame):
        """ ループ 終了処理 """  # {{{
        if frame is None:
            print("Can not get video frame")
            return False
            # }}}

    def go_get_master_mode(self):
        """ マスター画像取得モード 遷移 """  # {{{
        print("")
        print("Input key \"t\"")
        print("Go master mode")
        time.sleep(0.5)
        img = "master_source{}".format(self.extension)

        # 文字描画消去の為 再読込み
        get_flag, frame = self.cap.read()

        cv2.imwrite(img, frame)
        trim = tm.Trim(img, self.search, self.extension, self.path, mode=1)
        trim.trim()
        # }}}


def main():
    """ メインルーチン """
    # vimテスト用各変数 定義# {{{
    # イニシャル情報 出力
    print("")
    print("".center(print_col, "-"))
    print("INFORMATION".center(print_col, " "))
    print("".center(print_col, "-"))
    print("Default current directory:")
    print(os.getcwd().rjust(print_col, " "))
    print("")
    print("And then...")
    os.chdir("D:\OneDrive\Biz\Python\ImageProcessing")
    print(os.getcwd().rjust(print_col, " "))

    print("")
    print("〓" * int(print_col / 2))
    print("START MAIN".center(print_col, " "))
    print("〓" * int(print_col / 2))
    print("")
    # import pdb; pdb.set_trace()

    # path = "D:\\OneDrive\\Biz\\Python\\ImageProcessing"
    # pic_smpl_1 = "D:\\OneDrive\\Biz\\Python\\ImageProcessing\\tpl_1.png"
    # pic_smpl_2 = "D:\\OneDrive\\Biz\\Python\\ImageProcessing\\tpl_2.png"
# }}}

    # テンプレートマッチング テスト# {{{
    cip = ImageProcessing()
    cip.run("Raw capture", "masterImage")
    print("Image processing end...")
    # }}}

#     # 静止画取得 テスト# {{{
#     gim = GetImage(pic_smpl_1)
#     gim2 = GetImage("tpl_3.png")
#     # gim.diplay("Tes1", 0, 0)
#     gim2.display("Tes2", 0, 0)
#     print("Main loop end...")
# # }}}

# # 動画取得 テスト# {{{
#     cav = CapVideo()
#     cav.get_video("Capture_test")
#     frame_test = cav.frame
#     if frame_test is None:
#         gm = GetImage(pic_smpl_1)
#         gm.get_image()
#     name = "Test"
#     Image = cv2.imread(pic_smpl_2)
#     cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
#     cv2.imshow(name, Image)
#     cv2.imshow(name, frame_test)
#     # 仮の出力保持処理！！！
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#     image = cv2.imread("tpl_2.png")
#     cim = ConvertImage()
#     cim.adaptive_threashold(image, "Adaptive Threashold", 0)
#     print("Sudah cap")
# # }}}

    # # ドキュメントストリング# {{{
    # print(GetImage.__doc__)
    # print(help(__name__))
    # }}}

if __name__ == '__main__':
    main()
