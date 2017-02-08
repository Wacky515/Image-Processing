# !/usr/bin/python
# -*- coding: utf-8 -*-
# --------------------------------------------------  # {{{
# Name:        tplmatching.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     23/03/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10001
# --------------------------------------------------
# }}}
""" テンプレートマッチングによる画像処理 """
# FIXME:
#     Macではtemplate保存後にMatchingに戻らない

# TODO:
#     "module" の指定は72行移行に統一する（"trim.py" も同様）
#     "path" の結合は "os.path.join()" を使用する
#     自作moduleのインポート方法 改善する
#     しきい値 手動入力にする
#     アイコン 作成
#     ソフト名 正式にする

#     画像出力ウィンドウの位置を定義（固定）する
#     複数索敵・多段式判定を実装する
#     -> インスタンスをイテレートする？
#     色識別 実装
#     関数名は動詞にする

# DONE:  # {{{
#     template画像が存在しないとtemplate読み込みエラー
#     ソース画像を保存できない！！！
#     変数は "[大区分/固有]_[小区分/汎用]"
#     メインループのネストが深すぎる
#     各処理をメソッドに切出す
#     デフォルト引数は "None" にする
#     "matchTemplate" の "TM_CCOEFF_NORMED" は正規化する必要があるのか調査
#     "***_NORMED"以外は正規化している
#     Python3系 対応！！！
#     Unicode文字リテラルを " u"body" " -> " "body" " に変更
#     文字列の埋込を % 形式から format 形式に変更
#     "print" -> "print()" に変更
#     シリアル通信機能 実装
#     __inin__.pyの作成
#     GUI 実装
#     OCR 実装（該当の module を発見し、import 実験まで完了）
#     バーコード読取り機能 実装
#     （該当の module を発見し、import 実験まで完了）
#     "pprint" を使用する

# ABORT:
#     ワークを動体検出後に判定開始する
#     ワーク検出は背景差分で行う
# }}}

# モジュール インポート# {{{
import os
import sys
import time
# import glob
# !!!: ↓の "numpy" は消さない！！！
import numpy as np
from pprint import pprint

# import unittest

import cv2
import cv2.cv as cv

try:
    cdir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(cdir)

    sys.path.append(os.path.join("..", "SaveData"))
    sys.path.append(os.path.join("..", "Sound"))
    sys.path.append(os.path.join("..", "Serial"))

    import trim as tm
    import savedata as sd
    import judgesound as js
    import serialcom as sc

# TODO: ここ以降は改善必須
except:
    print("Can not find custum module")
    print("Add default search path:")
    pprint(sys.path)
    print("")

    try:
        sys.path.append("D:\OneDrive\Biz\Python")
        sys.path.append("D:\OneDrive\Biz\Python\SaveData")
        sys.path.append("D:\OneDrive\Biz\Python\Sound")
        sys.path.append("D:\OneDrive\Biz\Python\Serial")

        import trim as tm
        import savedata as sd
        import judgesound as js
        import serialcommun as sc

    except:
        try:
            sys.path.append("/Users/wacky515/OneDrive/Biz/Python")
            sys.path.append("/Users/wacky515/OneDrive/Biz/Python/SaveData")
            sys.path.append("/Users/wacky515/OneDrive/Biz/Python/Sound")
            sys.path.append("/Users/wacky515/OneDrive/Biz/Python/Serial")

            import trim as tm
            import savedata as sd
            import judgesound as js
            import serialcommun as sc

        except:
            sys.path.append("~/Python")
            sys.path.append("~/Python/SaveData")
            sys.path.append("~/Python/Sound")
            sys.path.append("~/Python/Serial")

            import trim as tm
            import savedata as sd
            import judgesound as js
            import serialcommun as sc

        # FIXME:
        finally:
            # cdir = os.path.abspath(os.path.dirname(__file__))

            # sys.path.append(os.path.join("", cdir, "SaveData"))
            # sys.path.append(os.path.join("", cdir, "Sound"))
            # sys.path.append(os.path.join("", cdir, "Serial"))
            sys.path.append(os.path.join("..", "SaveData"))
            sys.path.append(os.path.join("..", "Sound"))
            sys.path.append(os.path.join("..", "Serial"))

            import trim as tm
            import savedata as sd
            import judgesound as js
            # import serialcommun as sc
            import serialcommun as sc

    print("And then...")
    pprint(sys.path)

# sysモジュール リロード
reload(sys)

# デフォルトの文字コード 出力
sys.setdefaultencoding("utf-8")
# }}}

print_col = 50
save_lim = 100


def terminate(name_cap=None, time_wait=None):
    """ 画面出力 終了処理 """  # {{{
    if time_wait is None:
        time_wait = 33

    cv2.waitKey(time_wait)
    # name_cap [None: 静止画, それ以外: 動画]
    if name_cap is not None:
        name_cap.release
    cv2.destroyAllWindows()

    print("")
    print("Terminated...")
    sys.exit("System end")
# }}}


class GetImage:
    """ 画像・動画 取得クラス """  # {{{
    def __init__(self, image):
        self.image = image

    def get_image(self, conversion=None):
        """ 画像・動画 読込み """
        if conversion is None:
            conversion = 1

        # 画像取得
        try:
            image = cv2.imread(self.image, conversion)
            return image
        except:
            print("Image data is not found...")
            return False

    def display(self, window_name, image=None, _type=None):
        """ 画像・動画 画面出力 """
        if image is None:
            image = self.image

        # 静止画無し 処理 ← "is None" にした 動作確認！！！
        # _type [None: 静止画, それ以外: 動画]
        if image is None and _type is None:
            image = self.get_image()
            print("Go get image...")

        # TODO: "imshow" ウィンドウ幅 下限設定
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_name, image)
        print("Display {} image...".format(window_name))

        if _type is None:
            # 静止画の出力保持処理
            terminate()
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
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Convert grayscale...")
        print("")

        return gray

    def adaptive_threashold(self, image, algo=None, method=None):
        """ 適応的二値化 変換処理 """
        if algo is None:
            algo = 1
        if method is None:
            method = 0
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

        cat = cv2.adaptiveThreshold
        adpth = cat(gray, THRESH_MAX, eval(THRESH_ALGOS[algo]),
                    eval(self.THRESH_METHODS[method]), area_calc, subtract)
        print("Convert adaptive threashold...")
        print("")

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

        cvf = cv2.bilateralFilter
        blr = cvf(gray, area_calc, color_sigma, metric_sigma)
        print("Bilateral filtering...")
        print("")

        return blr

    def discriminantanalyse(self, image,
                            thresh_std=None, method=None):
        """ 判別分析法 処理 """
        if thresh_std is None:
            thresh_std = 128
        if method is None:
            method = 5
        blr = self.bilateral_filter(image)
        # 最大閾値
        THRESH_MAX = 255

        cth = cv2.threshold
        ret, dcta = cth(blr, thresh_std,
                        THRESH_MAX, eval(self.THRESH_METHODS[method]))
        print("Discriminant analysing...")
        print("")

        return dcta

    def binarize(self, image, thresh_std=None, method=None):
        """ 二値化 処理 """
        if thresh_std is None:
            thresh_std = 128
        if method is None:
            method = 1
        blr = self.bilateral_filter(image)
        # 最大閾値
        THRESH_MAX = 255

        cth = cv2.threshold
        ret, binz = cth(blr, thresh_std,
                        THRESH_MAX, eval(self.THRESH_METHODS[method]))
        print("Binarizing...")
        print("")

        return binz

    def normalize(self, image, alpha=None, beta=None):
        """ ノルム正規化 処理 """
        if alpha is None:
            alpha = 0
        if beta is None:
            beta = 1
        # alpha、beta 解説# {{{
        # TODO: わからんから図書館で資料を借りる！！！
        # TODO: 特にアルファ、ベータの数値の意味合いと妥当性！！！
        # alpha:ノルム正規化の場合、正規化されるノルム値
        #        範囲正規化の場合、下界
        # beta:ノルム正規化の場合、不使用
        #        範囲正規化の場合、の上界
        # }}}

        algo = cv2.NORM_MINMAX
        norm = cv2.normalize(image, image, alpha, beta, algo)
        print("Normalizing...")
        print("")

        return norm
# }}}


class Tplmatching:
    """ テンプレートマッチングクラス """
    cim = ConvertImage()

    def __init__(self):
        pass

    def tplmatch(self, source_image, master_image, algo=None):
        """ テンプレートマッチング 処理 """
        if algo is None:
            algo = 5
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

        cmt = cv2.matchTemplate
        match = cmt(source_image, master_image, eval(ALGOS[algo]))

        if ALGOS in ["cv2.TM_SQDIFF", "cv2.TM_CCORR", "cv2.TM_CCOEFF"]:
            # ノルム正規化 処理
            norm = self.cim.normalize(match)
            # 類似度の最小・最大値と各座標 取得
            val_min, val_max, loc_min, loc_max = cv2.minMaxLoc(norm)
        else:
            val_min, val_max, loc_min, loc_max = cv2.minMaxLoc(match)

        return match, val_min, val_max, loc_min, loc_max

    def mask(self):
        """ マスク 処理（将来的に実装） """
        # 初回でマッチした近傍領域以外にマスク処理し、処理速度向上する
        # ただし索敵位置が変化しない事が前提
        pass

    def calc_detect_location(self, loc_input, image, loc_output=None):
        """ 捕捉座標 演算 """
        if loc_output is None:
            loc_output = "center"

        height, width, channel = image.shape

        # 中央座標 演算
        if loc_output == "center":
            div = 2
        # 右下座標 演算
        elif loc_output == "tail":
            div = 1
        coord = (loc_input[0] + width / div, loc_input[1] + height / div)

        return coord, height, width

    def show_detect_area(self, location, image, frame):
        """ 捕捉範囲 演算 """
        # 中央座標 演算
        coord, height, width = \
            self.calc_detect_location(location, image)

        left_up = (location[0], location[1])
        right_low = (location[0] + width, location[1] + height)
        detect_image = (frame[location[1]:location[1] + height,
                        location[0]:location[0] + width].copy())

        return detect_image, left_up, right_low


class ImageProcessing:
    """ メイン画像処理クラス """
    cim = ConvertImage()
    tmc = Tplmatching()
    jsd = js.JudgeSound()

    ciadp = cim.adaptive_threashold
    cidca = cim.discriminantanalyse
    cibiz = cim.binarize
    cinor = cim.normalize

    def __init__(self):  # {{{
        # 動画 取得
        self.cap = cv2.VideoCapture(0)

        # マッチ判定値
        self.obj_detect = 0.40
        self.val_ok = 0.70

        # OK/NG 表示固定flag
        self.judge_flag = True

        # OKと判定する時間
        self.ok_time = 2
        self.ok_count = 0

        # 正規化（強調表示）の強調度
        self.highlight = 4

        # Beep音 再生回数固定用 カウンタ
        self.beep_count = 0

        # 操作説明文
        self.text2 = "End: Long press \"e\" key"
        self.text3 = "Mastering: Long press \"m\" key"

        # 判定用 変数
        # self.frame_eval = None

        # 最大・最小の値と座標
        self.val_max = None
        self.loc_max = None
        self.loc_min = None

        # UnixとWindowsのデリミタ差異 補完
        if os.name != "nt":
            self.delimiter = "/"
        elif os.name == "nt":
            self.delimiter = "\\"

# }}}

    def run(self, window_name, name_master, port, printout,
            extension=None, dir_master=None, dir_log=None,
            model=None, destination=None):
        """ 動画取得 処理（メインルーチン） """  # {{{
        # デフォルト引数 指定  # {{{
        self.port = port
        self.printout = printout

        sgm = self.go_get_master_mode

        if extension is None:
            self.extension = ".png"
        else:
            self.extension = extension

        if dir_master is None:
            self.dir_master = "MasterImage"
        else:
            self.dir_master = dir_master

        if dir_log is None:
            self.dir_log = "LogImage"
        else:
            self.dir_log = dir_log

        if model is None:
            self.model = "C597A"
        else:
            self.model = model

        if destination is None:
            self.destination = "LABEL BATT-C597A/J-CA"
        else:
            self.destination = destination
# }}}

        # 処理開始 標準出力  # {{{
        print("-" * print_col)
        print("START TEMPLATE MATCHING".center(print_col, " "))
        print("-" * print_col)
        print("")

        print(" SEARCH MASTER MODE ".center(print_col, "*"))
        print("")

        cwd = os.getcwd()
        path_master = cwd + self.delimiter + self.dir_master

        print("Master directory:")
        print(path_master.rjust(print_col, " "))
        print("")
# }}}

        # 検索するマスター画像 名前・パス 表示  # {{{
        search_master_file = str(name_master) + "_****" + str(self.extension)
        search_master_path = \
            str(path_master) + self.delimiter + search_master_file
        print("Search master file name: " + search_master_file)
        print("Search master path: " + search_master_path)
        print("")
# }}}

        # !!!: 複数探査の時はここの "sda" をイテレート処理
        # 枝番最大のマスター画像 取得  # {{{
        self.sda = sd.SaveData(name_master, path_master)
        set_num_master, get_num_master, get_master_flag = \
            self.sda.get_name_max(self.extension)
        print(" RETURN TEMPLATE MATCHING ".center(print_col, "*"))
        print("Get master flag: {}".format(get_master_flag))
        print("")
# }}}

        # マスター画像有無 判定  # {{{
        if get_master_flag is False:
            print("Master is none")

            # マスター画像取得モード 遷移
            while get_master_flag is False:
                get_num_master, get_master_flag = \
                    sgm(name_master, self.extension, path_master)
# }}}

        # イニシャルのマッチしたマスター画像 名前・パス 表示  # {{{
        master_file = str(get_num_master) + str(self.extension)
        master_path = str(path_master) + self.delimiter + master_file

        print("Get master name: " + str(get_num_master))
        print("Get master extension: " + str(self.extension))
        print("Master path: " + master_path)
        print("")
# }}}
        # !!!: イテレート処理予定 ここまで

        # キャプチャ 開始
        self.get_camera_image_init(window_name)

        # !!!: ここから
        count = 0
        while True:
            if count == 0:
                time.sleep(0.1)
                print("Initial delay")

            # キャプチャとキャプチャエラー 判定
            get_flag, frame = self.cap.read()

            if self.check_get_flag(get_flag):
                break
            if self.check_get_frame(frame):
                continue

            print("Capture is running...")
            print("")

            count += 1

            # マスター画像 セット
            master_file = str(get_num_master) + str(self.extension)
            master_path = str(path_master) + self.delimiter + master_file
            master = cv2.imread(str(master_path), 1)

            print("Master name: " + str(get_num_master))
            print("Master extension: " + str(self.extension))
            print("Master path: " + master_path)
            print("")

            # テンプレートマッチング イテレート処理
            # !!!: 複数探査の時はここのタプルにマスターを入れる
            # 評価用 処理リスト
            methods = [
                    ["Row", None],
                    # ["Adaptive threashold", self.ciadp],
                    # ["Discriminant analyse", self.cidca],
                    # ["Bilateral filter", self.cibiz]
                    ]

            # イテレート処理
            for method in methods:
                if method[1] is not None:
                    frame_eval = method[1](frame)
                    master_eval = method[1](master)
                else:
                    frame_eval = frame
                    master_eval = master

                # テンプレートマッチング 処理
                mch, self.val_min, self.val_max, self.loc_min, self.loc_max = \
                    self.tmc.tplmatch(frame_eval, master_eval)
                match = mch

                # マッチ領域 トリム処理
                detect_eval, left_up, right_low = \
                    self.tmc.show_detect_area(self.loc_max, master, frame)

                # 検出領域に操作領域と同じ画像処理 実行
                if method[1] is not None:
                    detect_eval = method[1](detect_eval)

                # OK/NG 判定
                self.judge_image(frame_eval, left_up, right_low)

                # 評価処理 画面表示
                scd = self.cim.display
                # scd(str(method[0] + " frame"), self.frame_eval, 1)
                scd(str(method[0] + " master"), master_eval, 1)
                scd("Detected " + str(method[0]), detect_eval, 1)

                # 捕捉範囲 正規化（捕捉範囲 強調表示用）
                norm = self.cinor(match)
                norm_eval = norm ** self.highlight
                # frameよりmaster分縮む
                self.cim.display("Normalize " + str(method[0]), norm_eval, 1)

                # 操作方法説明文 画面表示
                sdo = self.display_operation
                sdo(frame, window_name, self.text2, self.text3)

                # 類似度 標準出力
                self.print_simil(self.val_max, method)

            # "m" 押下 マスター画像取得モード 遷移
            if cv2.waitKey(33) == ord("m"):
                print("Input key \"m\"")
                print("Go get master")
                print("")
                get_num_master, get_master_flag = \
                    sgm(name_master, self.extension, path_master)

            # "e" 押下 終了処理
            if cv2.waitKey(33) == ord("e"):
                print("Input key \"e\"")
                print(" END PROCESS ".center(print_col, "*"))
                print("")
                break
            # }}}

    def get_camera_image_init(self, window_name):
        """ カメラから動画取得 """  # {{{
        # キャプチャ イニシャルディレイ
        time.sleep(0.1)
        print("Camera open check delay")
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
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
# }}}

    def check_get_flag(self, flag):
        """ 動画取得ミス時 スキップ処理 """  # {{{
        if flag is False:
            print("Can not get end flag")
            return True
            # }}}

    def check_get_frame(self, frame):
        """ ループ 終了処理 """  # {{{
        if frame is None:
            print("Can not get video frame")
            return True
            # }}}

    def judge_image(self, image, left_up, right_low):
        """ ワーク 検出・判定処理 """  # {{{
        self.image = image
        self.left_up = left_up
        self.right_low = right_low
        ok_pass = 0

        self.trim = tm.Trim(image, None, None, None, 1)

        # ワーク検知 判定
        if self.val_max > self.obj_detect:

            # ワーク検知 処理
            # モード 画面出力
            twt = self.trim.write_text
            msg = "Matching..."
            msg_height, msg_base = twt(msg, (0, "height"), offset=(0, 5))
            self.msg_origin = (0, 15 + msg_base)

            # *秒間OKで画面表示
            self.ok_count += 1
            if self.ok_count == 1:
                self.ok_start = time.time()
                print("Start OK time: " + str(self.ok_start))  # {{{
                print("")  # }}}
            elif self.ok_count > 1:
                ok_pass = time.time() - self.ok_start
                print("Start OK time: " + str(self.ok_start))  # {{{
                print("Pass OK time: " + str(round(ok_pass, 2)) + "[sec]")
                print("OK frame count: " + str(self.ok_count))
                print("")  # }}}

            # 検知時間 判定
            if ok_pass > self.ok_time:
                # OK/NG 判定処理
                if self.val_max > self.val_ok and self.judge_flag is True:
                    self.judge_ok()
                else:
                    self.judge_ng()

        # 検索中 表示
        # if self.val_max < self.obj_detect:
        else:
            self.trim.write_text("Searching...", (0, "height"), offset=(0, 5))
            self.init_judge_param()
# }}}

    def judge_ok(self):
        """ 判定OK 処理 """  # {{{
        self.beep_count += 1

        # "OK" 画面表示
        stwt = self.trim.write_text
        stwt("OK", (0, "height"), 2, "white", "green", 5, 4, self.msg_origin)

        # 検出位置矩形 画面表示
        stdr = self.trim.draw_rectangle
        stdr(self.left_up, self.right_low, "white", "green")

        # 類似度 表示
        similarity = round(self.val_max * 100, 1)
        sim = str(similarity) + "%"
        coord = (self.right_low[0], "height")
        offset = (0, self.right_low[1] + 5)
        stwt(sim, coord, scale=0.6, color_out="white", color_in="green",
             thickness_out=3, thickness_in=2, offset=offset)

        # OK音 音声出力
        if self.beep_count == 2:
            self.jsd.beep_ok()

            # OKログ 出力
            sda_ok_image = sd.SaveData("ok_image", self.dir_log)
            sda_ok_text = sd.SaveData("judge_log", os.getcwd())
            sisi = sda_ok_image.save_image
            sisi(self.image, self.extension, save_lim=save_lim)
            stst = sda_ok_text.save_text
            stst("OK, {}, {}, {}, {}".format(self.val_max, self.loc_max,
                                             self.val_min, self.loc_min))

            print("Set port: {}".format(self.port))
            print(self.destination)
            print("{}".format(self.printout[self.model][self.destination]))
            print("")

            try:
                src = sc.SerialCom()
                sst = src.send_tsc
                sst(self.printout[self.model][self.destination], self.port)
            except:
                print(" BARCODE PRINT OUT ERROR ".center(print_col, "*"))
                print("")
# }}}

    def judge_ng(self):
        """ 判定NG 処理 """  # {{{
        self.beep_count += 1
        self.judge_flag = False

        # NG 画面表示
        stwt = self.trim.write_text
        stwt("NG", (0, "height"), 2, "white", "red", 5, 4, self.msg_origin)

        # NG音 音声出力
        if self.beep_count == 2:
            self.jsd.beep_ng()

            # NGログ 出力
            sda_ng_image = sd.SaveData("ng_image", self.dir_log)
            sda_ng_text = sd.SaveData("judge_log", os.getcwd())
            sisi = sda_ng_image.save_image
            sisi(self.image, self.extension, save_lim=save_lim)
            stst = sda_ng_text.save_text
            stst("NG, {}, {}, {}, {}" .format(self.val_max, self.loc_max,
                                              self.val_min, self.loc_min))
# }}}

    def init_judge_param(self):
        """ 判定諸元 初期化 """  # {{{
        self.ok_count = 0
        self.ok_start = 0
        self.beep_count = 0
        self.judge_flag = True
# }}}

    def get_still_image(self):
        """ マスター画像取得モード 遷移 """  # {{{
        ext = self.extension
        print("Get still image")
        print("")

        time.sleep(0.1)
        image = "{}{}master_source{}".format(self.path, self.delimiter, ext)
        print("Get master name: {}".format(image))

        # 文字描画消去の為 再読込み
        get_flag, frame = self.cap.read()

        cv2.imwrite(image, frame)
        trim = tm.Trim(image, self.search, ext, self.path, end_process=1)
        trim.trim()
        # }}}

    def display_operation(self, frame, window_name, text1, text2):
        """ 操作方法説明文 画面表示 """  # {{{
        # 操作方法説明文 表示位置 取得
        text_offset = 10
        baseline = frame.shape[0] - text_offset
        origin = 1, baseline

        # 操作方法説明文 表示
        trim = tm.Trim(frame, None, None, None, 1)
        text_height = trim.write_text(text1, origin)
        coor_x = origin[0]
        coor_y = origin[1] - text_offset - text_height[1]
        trim.write_text(text2, (coor_x, coor_y))

        # メイン画面 表示
        self.cim.display(window_name, frame, 1)
        # import pdb; pdb.set_trace()
# }}}

    def go_get_master_mode(self, image, extension, path):
        """ マスター画像取得モード 遷移 """  # {{{
        print("Go get master mode")
        print("")
        time.sleep(0.1)

        # TODO: 複数探査の時はここの "sda" をイテレート処理！！！
        self.get_master(image, extension, path, 1)
        set_name, get_name, get_flag = \
            self.sda.get_name_max(extension)
        # TODO: イテレート処理予定 ここまで！！！
        cv2.destroyAllWindows()

        print("Get master name: " + str(get_name))

        return get_name, get_flag
# }}}

    # TODO: 見直し(main loop で切出したメソッドに代替する)！！！
    def get_master(self, search, extension, path, mode=None):
        """ マスター画像 読込み """  # {{{
        self.search = search
        self.extension = extension
        self.path = path

        name = "Get master image"
        text2 = "Quit: Long press \"q\" key"
        text3 = "Trimming: Long press \"t\" key"

        # 処理開始 標準出力  # {{{
        print("-" * print_col)
        print(" START GET MASTER MODE ".center(print_col, "*"))
        print("-" * print_col)
        print("Search master name: " + str(search))
        print("")
# }}}

        # 判定諸元 初期化
        self.init_judge_param()
        # キャプチャ 開始
        self.get_camera_image_init(name)

        count = 0
        while True:
            if count == 0:
                time.sleep(0.1)
                print("Initial delay")

            # キャプチャとキャプチャエラー 判定
            get_flag, frame = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            # マスター画像取得モード 直接遷移
            if mode is not None:
                self.get_still_image()
                break

            # 操作方法説明文 画面表示
            sdo = self.display_operation
            frame_draw = frame
            sdo(frame_draw, name, text2, text3)

            # # TODO: 見直し(main loop で切出したメソッドに代替する)！！！
            # # 操作方法説明文 表示位置 取得
            # text_offset = 10
            # baseline = frame.shape[0] - text_offset
            # origin = 1, baseline

            # # TODO: 見直し(main loop で切出したメソッドに代替する)！！！
            # # 操作方法説明文 表示
            # frame_draw = frame
            # trim = tm.Trim(frame_draw, search, extension, path, 1)
            # text_height = trim.write_text(text2, origin)
            # trim.write_text(text3,
            #                 (origin[0],
            #                  origin[1] - text_offset - text_height[1]))
            # self.cim.display(name, frame_draw, 1)

            print("Master capture")
            count += 1

            # "t" 押下 マスター画像取得モード 遷移
            if cv2.waitKey(33) == ord("t"):
                print("Input key \"t\"")
                print("")
                self.get_still_image()

            # "q" 押下 終了処理
            if cv2.waitKey(33) == ord("q"):
                print("Input key \"q\"")
                time.sleep(0.5)
                print(" END GET MASTER MODE ".center(print_col, "*"))
                print("")
                # import pdb; pdb.set_trace()
                break
# }}}

    def print_simil(self, val_max, method):
        """ 類似度 標準出力 """  # {{{
        simil_max = str(round(val_max * 100, 2)) + "%"
        simil_min = str(round(self.val_min * 100, 2)) + "%"
        print("")

        print("Method: {}".format(method[0]))

        print("Max similarity:")
        print(str(simil_max.rjust(print_col, " ")))
        print(str(self.loc_max).rjust(print_col, " "))

        print("Min similarity:")
        print(str(simil_min.rjust(print_col, " ")))
        print(str(self.loc_min).rjust(print_col, " "))
        print("")
# }}}


def main():
    """ メインルーチン """
    # Vimテスト用各変数 定義# {{{

    # イニシャル情報 出力
    print("".center(print_col, "-"))
    print("INFORMATION".center(print_col, " "))
    print("".center(print_col, "-"))
    print("Default current directory:")
    print(os.getcwd().rjust(print_col, " "))
    print("")

    print("And then...")
    try:
        os.chdir("D:\OneDrive\Biz\Python\ImageProcessing")
    except:
        try:
            os.chdir("/Users/wacky515/OneDrive/Biz/Python/ImageProcessing")
        except:
            cdir = os.path.abspath(os.path.dirname(__file__))
            # os.chdir("~/Python/ImageProcessing")

    # print(os.getcwd().rjust(print_col, " "))

    print("")
    print(u"〓" * int(print_col / 2))
    print("START MAIN".center(print_col, " "))
    print(u"〓" * int(print_col / 2))
    print("")
    # import pdb; pdb.set_trace()
# }}}

    # テンプレートマッチング テスト# {{{
    # 機種固有設定は実行ファイル上で "config" を作成しPickle化する
    port = 2
    printout = {"C597A": {
                "LABEL BATT-C597A/J-CA": "1AG6P4S2000-ABA",
                "LABEL BATT-C597A/C-CA": "1AG6P4S2000-BBA",
                "LABEL BATT-C597A/OTCA-S1P": "1AG6P4S2000--BA"
                }}

    cip = ImageProcessing()
    cip.run("Raw capture", "masterImage", port, printout)
    print("Image processing end...")
# }}}

    # 静止画取得 テスト# {{{
    # gim = GetImage(pic_smpl_1)
    # gim2 = GetImage("tpl_3.png")
    # # gim.diplay("Tes1", 0, 0)
    # gim2.display("Tes2", 0, 0)
    # print("Main loop end...")
# }}}

    # 動画取得 テスト# {{{
    # cav = GetImage()
    # cav.get_image("Capture_test")
    # frame_test = cav.frame
    # if frame_test is None:
    #     gm = GetImage(pic_smpl_1)
    #     gm.get_image()
    # name = "Test"
    # Image = cv2.imread(pic_smpl_2)
    # cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    # cv2.imshow(name, Image)
    # cv2.imshow(name, frame_test)
    # # 仮の出力保持処理！！！
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # image = cv2.imread("tpl_2.png")
    # cim = ConvertImage()
    # cim.adaptive_threashold(image, "Adaptive Threashold", 0)
    # print("Sudah cap")
# }}}

    # # ドキュメントストリング# {{{
    # print(GetImage.__doc__)
    # print(help(__name__))
    # }}}

if __name__ == "__main__":
    main()
