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
""" �e���v���[�g�}�b�`���O�ɂ��摜���� """

# TODO:
# �������l �蓮���͂ɂ���
# �A�C�R�� �쐬
# �\�t�g�� �����ɂ���

# �摜�o�̓E�B���h�E�̈ʒu���`�i�Œ�j����
# �������G�E���i���������������
# -> �C���X�^���X���C�e���[�g����H
# �F���� ����
# �֐����͓����ɂ���

# DONE:  # {{{
# �ϐ��� "[��敪/�ŗL]_[���敪/�ėp]"
# ���C�����[�v�̃l�X�g���[������
# �e���������\�b�h�ɐ؏o��
# �f�t�H���g������ "None" �ɂ���
# "matchTemplate" �� "TM_CCOEFF_NORMED" �͐��K������K�v������̂�����
# "***_NORMED"�ȊO�͐��K�����Ă���
# Python3�n �Ή��I�I�I
# Unicode�������e������ " u"body" " -> " "body" " �ɕύX
# ������̖����� % �`������ format �`���ɕύX
# "print" -> "print()" �ɕύX
# �V���A���ʐM�@�\ ����
# __inin__.py�̍쐬
# GUI ����
# OCR �����i�Y���� module �𔭌����Aimport �����܂Ŋ����j
# �o�[�R�[�h�ǎ��@�\ ����
# �i�Y���� module �𔭌����Aimport �����܂Ŋ����j
# "pprint" ���g�p����

# ABORT:
# ���[�N�𓮑̌��o��ɔ���J�n����
# ���[�N���o�͔w�i�����ōs��
# }}}

# ���W���[�� �C���|�[�g# {{{
import os
import sys
import time
# import glob
# !!!: ���� "numpy" �͏����Ȃ��I�I�I
import numpy as np
from pprint import pprint

# import unittest

import cv2
import cv2.cv as cv

try:
    import trim as tm
    import savedata as sd
    import judgesound as js
    import serialcom as sc
except:
    print("Can not find custum module")
    print("Add default search path:")
    pprint(sys.path)
    print("")

    print("And then...")
    sys.path.append("D:\OneDrive\Biz\Python")
    sys.path.append("D:\OneDrive\Biz\Python\SaveData")
    sys.path.append("D:\OneDrive\Biz\Python\Sound")
    sys.path.append("D:\OneDrive\Biz\Python\Serial")

    import trim as tm
    import savedata as sd
    import judgesound as js
    import serialcom as sc

    pprint(sys.path)

# sys���W���[�� �����[�h
reload(sys)

# �f�t�H���g�̕����R�[�h �o��
sys.setdefaultencoding("utf-8")
# }}}

print_col = 50
save_lim = 100


def terminate(name_cap=None, time_wait=None):
    """ ��ʏo�� �I������ """  # {{{
    if time_wait is None:
        time_wait = 33

    cv2.waitKey(time_wait)
    # name_cap [None: �Î~��, ����ȊO: ����]
    if name_cap is not None:
        name_cap.release
    cv2.destroyAllWindows()

    print("")
    print("Terminated...")
    sys.exit("System end")
# }}}


class GetImage:
    """ �摜�E���� �擾�N���X """  # {{{
    def __init__(self, image):
        self.image = image

    def get_image(self, conversion=None):
        """ �摜�E���� �Ǎ��� """
        if conversion is None:
            conversion = 1

        # �摜�擾
        try:
            image = cv2.imread(self.image, conversion)
            return image
        except:
            print("Image data is not found...")
            return False

    def display(self, window_name, image=None, _type=None):
        """ �摜�E���� ��ʏo�� """
        if image is None:
            image = self.image

        # �Î~�斳�� ���� �� "is None" �ɂ��� ����m�F�I�I�I
        # _type [None: �Î~��, ����ȊO: ����]
        if image is None and _type is None:
            image = self.get_image()
            print("Go get image...")

        # TODO: "imshow" �E�B���h�E�� �����ݒ�
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_name, image)
        print("Display {} image...".format(window_name))

        if _type is None:
            # �Î~��̏o�͕ێ�����
            terminate()
# }}}


class ConvertImage(GetImage):
    """ �摜�E���� �ϊ��N���X """  # {{{
    # 臒l���� ��@���X�g
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
        """ �O���[�X�P�[�� �ϊ����� """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Convert grayscale...")
        print("")

        return gray

    def adaptive_threashold(self, image, algo=None, method=None):
        """ �K���I��l�� �ϊ����� """
        if algo is None:
            algo = 1
        if method is None:
            method = 0
        gray = self.grayscale(image)
        # �K���I��l��(Adaptive Gaussian Thresholding) �p�����^��`# {{{
        # *** �K���I��l�� ��� ***
        # 1��f���ɁA�C�ӂ̋ߖT��f����ʂ�臒l���Z�o
        # }}}
        # �ő�臒l
        THRESH_MAX = 255
        # 臒l�Z�o�A���S���Y��# {{{
        # MeanC:        �C�ӂ̋ߖT��f���Z�p���ς�臒l���Z�o
        # GaussianC:    �C�ӂ̋ߖT��f��Gaussian�ɂ��d�ݕt��
        #               �i�ߖT���d���j�ő��a��臒l���Z�o
        # }}} """
        THRESH_ALGOS = ["cv2.ADAPTIVE_THRESH_MEAN_C",
                        "cv2.ADAPTIVE_THRESH_GAUSSIAN_C"]
        # �؎�鐳���`�̈�̉�f���i3�A5�A7... ��̂݁I�j
        area_calc = 7
        # ���Z�萔# {{{
        #   ���͂������F�̎��A���Z����臒l���Ӑ}�I�ɓˏo����
        #   �w�i�̈�̃m�C�Y�E�F��炬�̉e����ጸ����
        # }}}
        subtract = 4

        cat = cv2.adaptiveThreshold
        adpth = cat(gray, THRESH_MAX, eval(THRESH_ALGOS[algo]),
                    eval(self.THRESH_METHODS[method]), area_calc, subtract)
        print("Convert adaptive threashold...")
        print("")

        return adpth

    def bilateral_filter(self, image):
        """ �o�C���e�����t�B���^ ���� """
        gray = self.grayscale(image)
        # �؎�鐳���`�̈�̉�f���i3�A5�A7... ��̂݁I�j
        #   ���l���傫���قǂڂ₯��
        area_calc = 7
        # �F��Ԃɂ�����t�B���^�V�O�}
        #   �傫���Ȃ�ƐF�̗̈悪���傫���Ȃ�
        color_sigma = 12
        # ���W��Ԃɂ�����t�B���^�V�O�}
        #   �傫���Ȃ�Ƃ�艓���̉�f���m���e������
        metric_sigma = 3

        cvf = cv2.bilateralFilter
        blr = cvf(gray, area_calc, color_sigma, metric_sigma)
        print("Bilateral filtering...")
        print("")

        return blr

    def discriminantanalyse(self, image,
                            thresh_std=None, method=None):
        """ ���ʕ��͖@ ���� """
        if thresh_std is None:
            thresh_std = 128
        if method is None:
            method = 5
        blr = self.bilateral_filter(image)
        # �ő�臒l
        THRESH_MAX = 255

        cth = cv2.threshold
        ret, dcta = cth(blr, thresh_std,
                        THRESH_MAX, eval(self.THRESH_METHODS[method]))
        print("Discriminant analysing...")
        print("")

        return dcta

    def binarize(self, image, thresh_std=None, method=None):
        """ ��l�� ���� """
        if thresh_std is None:
            thresh_std = 128
        if method is None:
            method = 1
        blr = self.bilateral_filter(image)
        # �ő�臒l
        THRESH_MAX = 255

        cth = cv2.threshold
        ret, binz = cth(blr, thresh_std,
                        THRESH_MAX, eval(self.THRESH_METHODS[method]))
        print("Binarizing...")
        print("")

        return binz

    def normalize(self, image, alpha=None, beta=None):
        """ �m�������K�� ���� """
        if alpha is None:
            alpha = 0
        if beta is None:
            beta = 1
        # alpha�Abeta ���# {{{
        # TODO: �킩��񂩂�}���قŎ������؂��I�I�I
        # TODO: ���ɃA���t�@�A�x�[�^�̐��l�̈Ӗ������ƑÓ����I�I�I
        # alpha:�m�������K���̏ꍇ�A���K�������m�����l
        #        �͈͐��K���̏ꍇ�A���E
        # beta:�m�������K���̏ꍇ�A�s�g�p
        #        �͈͐��K���̏ꍇ�A�̏�E
        # }}}

        algo = cv2.NORM_MINMAX
        norm = cv2.normalize(image, image, alpha, beta, algo)
        print("Normalizing...")
        print("")

        return norm
# }}}


class Tplmatching:
    """ �e���v���[�g�}�b�`���O�N���X """
    cim = ConvertImage()

    def __init__(self):
        pass

    def tplmatch(self, source_image, master_image, algo=None):
        """ �e���v���[�g�}�b�`���O ���� """
        if algo is None:
            algo = 5
        # �ގ��x����A���S���Y�� ���# {{{
        # cv2.TM_SQDIFF    :�P�x�l�̍��̂Q��̍��v     �������قǗގ�
        # cv2.TM_CCORR     :�P�x�l�̑���               �傫���قǗގ�
        # cv2.TM_CCOEFF    :�P�x�l�̕��ς�����������   �傫���قǗގ�
        #                 �i�e���v���[�g�摜�ƒT���摜�̖��邳�ɍ��E����ɂ����j
        # cv2.TM_***_NORMED :��L���ꂼ��̐��K����
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
            # �m�������K�� ����
            norm = self.cim.normalize(match)
            # �ގ��x�̍ŏ��E�ő�l�Ɗe���W �擾
            val_min, val_max, loc_min, loc_max = cv2.minMaxLoc(norm)
        else:
            val_min, val_max, loc_min, loc_max = cv2.minMaxLoc(match)

        return match, val_min, val_max, loc_min, loc_max

    def mask(self):
        """ �}�X�N �����i�����I�Ɏ����j """
        # ����Ń}�b�`�����ߖT�̈�ȊO�Ƀ}�X�N�������A�������x���シ��
        # ���������G�ʒu���ω����Ȃ������O��
        pass

    def calc_detect_location(self, loc_input, image, loc_output=None):
        """ �ߑ����W ���Z """
        if loc_output is None:
            loc_output = "center"

        height, width, channel = image.shape

        # �������W ���Z
        if loc_output == "center":
            div = 2
        # �E�����W ���Z
        elif loc_output == "tail":
            div = 1
        coord = (loc_input[0] + width / div, loc_input[1] + height / div)

        return coord, height, width

    def show_detect_area(self, location, image, frame):
        """ �ߑ��͈� ���Z """
        # �������W ���Z
        coord, height, width = \
            self.calc_detect_location(location, image)

        left_up = (location[0], location[1])
        right_low = (location[0] + width, location[1] + height)
        detect_image = (frame[location[1]:location[1] + height,
                        location[0]:location[0] + width].copy())

        return detect_image, left_up, right_low


class ImageProcessing:
    """ ���C���摜�����N���X """
    cim = ConvertImage()
    tmc = Tplmatching()
    jsd = js.JudgeSound()

    ciadp = cim.adaptive_threashold
    cidca = cim.discriminantanalyse
    cibiz = cim.binarize
    cinor = cim.normalize

    def __init__(self):  # {{{
        # ���� �擾
        self.cap = cv2.VideoCapture(0)

        # �}�b�`����l
        self.obj_detect = 0.40
        self.val_ok = 0.70

        # OK/NG �\���Œ�flag
        self.judge_flag = True

        # OK�Ɣ��肷�鎞��
        self.ok_time = 2
        self.ok_count = 0

        # ���K���i�����\���j�̋����x
        self.highlight = 4

        # Beep�� �Đ��񐔌Œ�p �J�E���^
        self.beep_count = 0

        # ���������
        self.text2 = "End: Long press \"e\" key"
        self.text3 = "Mastering: Long press \"m\" key"

        # ����p �ϐ�
        # self.frame_eval = None

        # �ő�E�ŏ��̒l�ƍ��W
        self.val_max = None
        self.loc_max = None
        self.loc_min = None
# }}}

    def run(self, window_name, name_master, port, printout,
            extension=None, dir_master=None, dir_log=None,
            model=None, destination=None):
        """ ����擾 �����i���C�����[�`���j """  # {{{
        # �f�t�H���g���� �w��  # {{{
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

        # �����J�n �W���o��  # {{{
        print("-" * print_col)
        print("START TEMPLATE MATCHING".center(print_col, " "))
        print("-" * print_col)
        print("")

        print(" SEARCH MASTER MODE ".center(print_col, "*"))
        print("")

        cwd = os.getcwd()
        path_master = cwd + "\\" + self.dir_master
        print("Master directory:")
        print(path_master.rjust(print_col, " "))
        print("")
# }}}

        # ��������}�X�^�[�摜 ���O�E�p�X �\��  # {{{
        search_master_file = str(name_master) + "_****" + str(self.extension)
        search_master_path = str(path_master) + ".\\" + search_master_file
        print("Search master file name: " + search_master_file)
        print("Search master path: " + search_master_path)
        print("")
# }}}

        # !!!: �����T���̎��͂����� "sda" ���C�e���[�g����
        # �}�ԍő�̃}�X�^�[�摜 �擾  # {{{
        self.sda = sd.SaveData(name_master, path_master)
        set_num_master, get_num_master, get_master_flag = \
            self.sda.get_name_max(self.extension)
        print(" RETURN TEMPLATE MATCHING ".center(print_col, "*"))
        print("Get master flag: {}".format(get_master_flag))
        print("")
# }}}

        # �}�X�^�[�摜�L�� ����  # {{{
        if get_master_flag is False:
            print("Master is none")

            # �}�X�^�[�摜�擾���[�h �J��
            while get_master_flag is False:
                get_num_master = \
                    sgm(name_master, self.extension, path_master)
# }}}

        # �C�j�V�����̃}�b�`�����}�X�^�[�摜 ���O�E�p�X �\��  # {{{
        master_file = str(get_num_master) + str(self.extension)
        master_path = str(path_master) + ".\\" + master_file

        print("Get master name: " + str(get_num_master))
        print("Get master extension: " + str(self.extension))
        print("Master path: " + master_path)
        print("")
# }}}
        # !!!: �C�e���[�g�����\�� �����܂�

        # �L���v�`�� �J�n
        self.get_camera_image_init(window_name)

        # !!!: ��������
        count = 0
        while True:
            if count == 0:
                time.sleep(0.1)
                print("Initial delay")

            # �L���v�`���ƃL���v�`���G���[ ����
            get_flag, frame = self.cap.read()

            if self.check_get_flag(get_flag):
                break
            if self.check_get_frame(frame):
                continue

            print("Capture is running...")
            print("")

            count += 1

            # �}�X�^�[�摜 �Z�b�g
            master_file = str(get_num_master) + str(self.extension)
            master_path = str(path_master) + ".\\" + master_file
            master = cv2.imread(str(master_path), 1)

            print("Master name: " + str(get_num_master))
            print("Master extension: " + str(self.extension))
            print("Master path: " + master_path)
            print("")

            # �e���v���[�g�}�b�`���O �C�e���[�g����
            # !!!: �����T���̎��͂����̃^�v���Ƀ}�X�^�[������
            # �]���p �������X�g
            methods = [
                    ["Row", None],
                    # ["Adaptive threashold", self.ciadp],
                    # ["Discriminant analyse", self.cidca],
                    # ["Bilateral filter", self.cibiz]
                    ]

            # �C�e���[�g����
            for method in methods:
                if method[1] is not None:
                    frame_eval = method[1](frame)
                    master_eval = method[1](master)
                else:
                    frame_eval = frame
                    master_eval = master

                # �e���v���[�g�}�b�`���O ����
                mch, self.val_min, self.val_max, self.loc_min, self.loc_max = \
                    self.tmc.tplmatch(frame_eval, master_eval)
                match = mch

                # �}�b�`�̈� �g��������
                detect_eval, left_up, right_low = \
                    self.tmc.show_detect_area(self.loc_max, master, frame)

                # ���o�̈�ɑ���̈�Ɠ����摜���� ���s
                if method[1] is not None:
                    detect_eval = method[1](detect_eval)

                # OK/NG ����
                self.judge_image(frame_eval, left_up, right_low)

                # �]������ ��ʕ\��
                scd = self.cim.display
                # scd(str(method[0] + " frame"), self.frame_eval, 1)
                scd(str(method[0] + " master"), master_eval, 1)
                scd("Detected " + str(method[0]), detect_eval, 1)

                # �ߑ��͈� ���K���i�ߑ��͈� �����\���p�j
                norm = self.cinor(match)
                norm_eval = norm ** self.highlight
                # frame���master���k��
                self.cim.display("Normalize " + str(method[0]), norm_eval, 1)

                # ������@������ ��ʕ\��
                sdo = self.display_operation
                sdo(frame, window_name, self.text2, self.text3)

                # �ގ��x �W���o��
                self.print_simil(self.val_max, method)

            # "m" ���� �}�X�^�[�摜�擾���[�h �J��
            if cv2.waitKey(33) == ord("m"):
                print("Input key \"m\"")
                print("Go get master")
                print("")
                get_num_master = sgm(name_master, self.extension, path_master)

            # "e" ���� �I������
            if cv2.waitKey(33) == ord("e"):
                print("Input key \"e\"")
                print(" END PROCESS ".center(print_col, "*"))
                print("")
                break
            # }}}

    def get_camera_image_init(self, window_name):
        """ �J�������瓮��擾 """  # {{{
        # �L���v�`�� �C�j�V�����f�B���C
        time.sleep(0.1)
        print("Camera open check delay")
        if not self.cap.isOpened():
            print("Can not connect camera...")
            terminate()
            # �g���b�N�o�[ ��`(�ł��Ȃ�)�I�I�I# {{{
            #        bar_name = "Max threshold"
            #        print(thresh_max)
            # # �g���b�N�o�[ ����
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
        """ ����擾�~�X�� �X�L�b�v���� """  # {{{
        if flag is False:
            print("Can not get end flag")
            return True
            # }}}

    def check_get_frame(self, frame):
        """ ���[�v �I������ """  # {{{
        if frame is None:
            print("Can not get video frame")
            return True
            # }}}

    def judge_image(self, image, left_up, right_low):
        """ ���[�N ���o�E���菈�� """  # {{{
        self.image = image
        self.left_up = left_up
        self.right_low = right_low
        ok_pass = 0

        self.trim = tm.Trim(image, None, None, None, 1)

        # ���[�N���m ����
        if self.val_max > self.obj_detect:

            # ���[�N���m ����
            # ���[�h ��ʏo��
            twt = self.trim.write_text
            msg = "Matching..."
            msg_height, msg_base = twt(msg, (0, "height"), offset=(0, 5))
            self.msg_origin = (0, 15 + msg_base)

            # *�b��OK�ŉ�ʕ\��
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

            # ���m���� ����
            if ok_pass > self.ok_time:
                # OK/NG ���菈��
                if self.val_max > self.val_ok and self.judge_flag is True:
                    self.judge_ok()
                else:
                    self.judge_ng()

        # ������ �\��
        # if self.val_max < self.obj_detect:
        else:
            self.trim.write_text("Searching...", (0, "height"), offset=(0, 5))
            self.init_judge_param()
# }}}

    def judge_ok(self):
        """ ����OK ���� """  # {{{
        self.beep_count += 1

        # "OK" ��ʕ\��
        stwt = self.trim.write_text
        stwt("OK", (0, "height"), 2, "white", "green", 5, 4, self.msg_origin)

        # ���o�ʒu��` ��ʕ\��
        stdr = self.trim.draw_rectangle
        stdr(self.left_up, self.right_low, "white", "green")

        # �ގ��x �\��
        similarity = round(self.val_max * 100, 1)
        sim = str(similarity) + "%"
        coord = (self.right_low[0], "height")
        offset = (0, self.right_low[1] + 5)
        stwt(sim, coord, scale=0.6, color_out="white", color_in="green",
             thickness_out=3, thickness_in=2, offset=offset)

        # OK�� �����o��
        if self.beep_count == 2:
            self.jsd.beep_ok()

            # OK���O �o��
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
        """ ����NG ���� """  # {{{
        self.beep_count += 1
        self.judge_flag = False

        # NG ��ʕ\��
        stwt = self.trim.write_text
        stwt("NG", (0, "height"), 2, "white", "red", 5, 4, self.msg_origin)

        # NG�� �����o��
        if self.beep_count == 2:
            self.jsd.beep_ng()

            # NG���O �o��
            sda_ng_image = sd.SaveData("ng_image", self.dir_log)
            sda_ng_text = sd.SaveData("judge_log", os.getcwd())
            sisi = sda_ng_image.save_image
            sisi(self.image, self.extension, save_lim=save_lim)
            stst = sda_ng_text.save_text
            stst("NG, {}, {}, {}, {}" .format(self.val_max, self.loc_max,
                                              self.val_min, self.loc_min))
# }}}

    def init_judge_param(self):
        """ ���菔�� ������ """  # {{{
        self.ok_count = 0
        self.ok_start = 0
        self.beep_count = 0
        self.judge_flag = True
# }}}

    def get_still_image(self):
        """ �}�X�^�[�摜�擾���[�h �J�� """  # {{{
        ext = self.extension
        print("Get still image")
        print("")

        time.sleep(0.1)
        image = "{}\\master_source{}".format(self.path, ext)

        # �����`������̈� �ēǍ���
        get_flag, frame = self.cap.read()
        cv2.imwrite(image, frame)
        trim = tm.Trim(image, self.search, ext, self.path, end_process=1)
        trim.trim()
        # }}}

    def display_operation(self, frame, window_name, text1, text2):
        """ ������@������ ��ʕ\�� """  # {{{
        # ������@������ �\���ʒu �擾
        text_offset = 10
        baseline = frame.shape[0] - text_offset
        origin = 1, baseline

        # ������@������ �\��
        trim = tm.Trim(frame, None, None, None, 1)
        text_height = trim.write_text(text1, origin)
        coor_x = origin[0]
        coor_y = origin[1] - text_offset - text_height[1]
        trim.write_text(text2, (coor_x, coor_y))

        # ���C����� �\��
        self.cim.display(window_name, frame, 1)
        # import pdb; pdb.set_trace()
# }}}

    def go_get_master_mode(self, image, extension, path):
        """ �}�X�^�[�摜�擾���[�h �J�� """  # {{{
        print("Go get master mode")
        print("")
        time.sleep(0.1)

        # TODO: �����T���̎��͂����� "sda" ���C�e���[�g�����I�I�I
        self.get_master(image, extension, path, 1)
        set_name, get_name, get_flag = \
            self.sda.get_name_max(extension)
        # TODO: �C�e���[�g�����\�� �����܂ŁI�I�I
        cv2.destroyAllWindows()

        print("Get master name: " + str(get_name))

        return get_name
# }}}

    # TODO: ������(main loop �Ő؏o�������\�b�h�ɑ�ւ���)�I�I�I
    def get_master(self, search, extension, path, mode=None):
        """ �}�X�^�[�摜 �Ǎ��� """  # {{{
        self.search = search
        self.extension = extension
        self.path = path

        name = "Get master image"
        text2 = "Quit: Long press \"q\" key"
        text3 = "Trimming: Long press \"t\" key"

        # �����J�n �W���o��  # {{{
        print("-" * print_col)
        print(" START GET MASTER MODE ".center(print_col, "*"))
        print("-" * print_col)
        print("Search master name: " + str(search))
        print("")
# }}}

        # ���菔�� ������
        self.init_judge_param()
        # �L���v�`�� �J�n
        self.get_camera_image_init(name)

        count = 0
        while True:
            if count == 0:
                time.sleep(0.1)
                print("Initial delay")

            # �L���v�`���ƃL���v�`���G���[ ����
            get_flag, frame = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            # �}�X�^�[�摜�擾���[�h ���ڑJ��
            if mode is not None:
                self.get_still_image()
                break

            # ������@������ ��ʕ\��
            sdo = self.display_operation
            frame_draw = frame
            sdo(frame_draw, name, text2, text3)

            # # TODO: ������(main loop �Ő؏o�������\�b�h�ɑ�ւ���)�I�I�I
            # # ������@������ �\���ʒu �擾
            # text_offset = 10
            # baseline = frame.shape[0] - text_offset
            # origin = 1, baseline

            # # TODO: ������(main loop �Ő؏o�������\�b�h�ɑ�ւ���)�I�I�I
            # # ������@������ �\��
            # frame_draw = frame
            # trim = tm.Trim(frame_draw, search, extension, path, 1)
            # text_height = trim.write_text(text2, origin)
            # trim.write_text(text3,
            #                 (origin[0],
            #                  origin[1] - text_offset - text_height[1]))
            # self.cim.display(name, frame_draw, 1)

            print("Master capture")
            count += 1

            # "t"�L�[���� �}�X�^�[�摜�擾���[�h �J��
            if cv2.waitKey(33) == ord("t"):
                print("Input key \"t\"")
                print("")
                self.get_still_image()

            # "q"�L�[���� �I������
            if cv2.waitKey(33) == ord("q"):
                print("Input key \"q\"")
                time.sleep(0.5)
                print(" END GET MASTER MODE ".center(print_col, "*"))
                print("")
                # import pdb; pdb.set_trace()
                break
# }}}

    def print_simil(self, val_max, method):
        """ �ގ��x �W���o�� """  # {{{
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
    """ ���C�����[�`�� """
    # Vim�e�X�g�p�e�ϐ� ��`# {{{

    # �C�j�V������� �o��
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
    print("��" * int(print_col / 2))
    print("START MAIN".center(print_col, " "))
    print("��" * int(print_col / 2))
    print("")
    # import pdb; pdb.set_trace()
# }}}

    # �e���v���[�g�}�b�`���O �e�X�g# {{{
    # �@��ŗL�ݒ�͎��s�t�@�C����� "config" ���쐬��Pickle������
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

    # �Î~��擾 �e�X�g# {{{
    # gim = GetImage(pic_smpl_1)
    # gim2 = GetImage("tpl_3.png")
    # # gim.diplay("Tes1", 0, 0)
    # gim2.display("Tes2", 0, 0)
    # print("Main loop end...")
# }}}

    # ����擾 �e�X�g# {{{
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
    # # ���̏o�͕ێ������I�I�I
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # image = cv2.imread("tpl_2.png")
    # cim = ConvertImage()
    # cim.adaptive_threashold(image, "Adaptive Threashold", 0)
    # print("Sudah cap")
# }}}

    # # �h�L�������g�X�g�����O# {{{
    # print(GetImage.__doc__)
    # print(help(__name__))
    # }}}

if __name__ == "__main__":
    main()
