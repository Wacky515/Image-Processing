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
""" �e���v���[�g�}�b�`���O�ɂ��摜���� """

# TODO: OCR ����
# TODO: ���[�N�𓮑̌��o��ɔ���J�n����
# TODO: �������G�E���i���������������
# TODO: �֐����͓����ɂ���
# TODO: �ϐ��� "[��敪]_[���敪]"
# TODO: �o�̓E�B���h�E�̈ʒu���`����
# TODO: ���[�N���o�͔w�i�����ōs��
# TODO: �F���� ����
# TODO: GUI ����

# DONE: "matchTemplate" �� "TM_CCOEFF_NORMED" �͐��K������K�v������̂�����
#       "***_NORMED"�ȊO�͐��K�����Ă���

# DONE: Python3�n �Ή��I�I�I
# DONE: Unicode�������e������ " u"body" " -> " "body" " �ɕύX
# DONE: ������̖����� % �`������ format �`���ɕύX
# DONE: "print" -> "print()" �ɕύX

# ���W���[�� �C���|�[�g# {{{
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

import savedata as sd

# sys���W���[�� �����[�h
reload(sys)

# �f�t�H���g�̕����R�[�h �o��
sys.setdefaultencoding("utf-8")
# }}}

print_col = 50


def terminate(name_cap=0, time_wait=33):
    """ �o�͉摜 �I������ """  # {{{
    # name_cap: 0: �Î~�� 1: ����
    cv2.waitKey(time_wait)
    if name_cap != 0:
        name_cap.release
    cv2.destroyAllWindows()
    print("Terminated...")
    sys.exit()
# }}}


class GetImage:
    """ �摜�E���� �擾�N���X """  # {{{
    def __init__(self, image):
        self.image = image

    def get_image(self, conversion=1):
        """ �摜�E���� �Ǎ��� """
        try:
            image = cv2.imread(self.image, conversion)
            return image
        # �摜�擾 �G���[����
        except:
            print("Image data is not found...")
            return False

    def display(self, name_window, image, _type=1):
        """ �摜�E���� ��ʏo�� """
        # _type: 0: �Î~�� 1: ���� �؊���
        # �Î~�斳�����莞 ���� �� "is None" �ɂ��� ����m�F�I�I�I
        if image is None and _type == 0:
            print("Getting image...")
            image = self.get_image()
        print("Display {}s...".format(name_window))
        cv2.namedWindow(name_window, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(name_window, image)
        if _type == 0:
            # �Î~��̏o�͕ێ�����
            terminate(0, 0)
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
        print("Convert grayscale...")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    def adaptive_threashold(self, image, algo=1, method=0):
        """ �K���I��l�� �ϊ����� """
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
        # �K���I��l�� �ϊ�����
        print("Convert adaptive threashold...")
        cat = cv2.adaptiveThreshold
        adpth = cat(gray, THRESH_MAX, eval(THRESH_ALGOS[algo]),
                    eval(self.THRESH_METHODS[method]), area_calc, subtract)
        # adpth = cat(gray, THRESH_MAX, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    # cv2.THRESH_BINARY, area_calc, subtract)
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
        print("Bilateral filtering...")
        cvf = cv2.bilateralFilter
        blr = cvf(gray, area_calc, color_sigma, metric_sigma)
        return blr

    def discriminantanalyse(self, image,
                            thresh_std=128, method=5):
        """ ���ʕ��͖@ ���� """
        image = self.bilateral_filter(image)
        print("Discriminant analysing...")
        cth = cv2.threshold
        # �ő�臒l
        THRESH_MAX = 255
        ret, dcta = cth(image, thresh_std,
                        THRESH_MAX, eval(self.THRESH_METHODS[method]))
        return dcta

    def binarize(self, image, thresh_std=128, method=1):
        """ ��l�� ���� """
        image = self.bilateral_filter(image)
        print("Binarizing...")
        cth = cv2.threshold
        # �ő�臒l
        THRESH_MAX = 255
        ret, binz = cth(image, thresh_std,
                        THRESH_MAX, eval(self.THRESH_METHODS[method]))
        return binz

    def normalize(self, image, alpha=0, beta=1):
        """ �m�������K�� ���� """
        # alpha�Abeta ���# {{{
        # TODO: �킩��񂩂�}���قŎ������؂��I�I�I
        # TODO: ���ɃA���t�@�A�x�[�^�̐��l�̈Ӗ������ƑÓ����I�I�I
        # alpha:�m�������K���̏ꍇ�A���K�������m�����l
        #        �͈͐��K���̏ꍇ�A���E
        # beta:�m�������K���̏ꍇ�A�s�g�p
        #        �͈͐��K���̏ꍇ�A�̏�E
        # }}}
        algo = cv2.NORM_MINMAX
        print("Normalizing...")
        norm = cv2.normalize(image, image, alpha, beta, algo)
        return norm
# }}}


class Tplmatching:
    """ �e���v���[�g�}�b�`���O �N���X """
    def __init__(self):
        self.ci = ConvertImage()

    def tplmatch(self, image, tpl, algo=5):
        """ �e���v���[�g�}�b�`���O ���� """
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
        match = cv2.matchTemplate(image, tpl, eval(ALGOS[algo]))
        if ALGOS in ["cv2.TM_SQDIFF", "cv2.TM_CCORR", "cv2.TM_CCOEFF"]:
            # �m�������K�� ����
            norm = self.ci.normalize(match)
            # �ގ��x�̍ŏ��E�ő�l�Ɗe���W �擾
            value_min, value_max, loc_min, loc_max = cv2.minMaxLoc(norm)
        else:
            value_min, value_max, loc_min, loc_max = cv2.minMaxLoc(match)
        return match, value_min, value_max, loc_min, loc_max

    def mask(self):
        """ �}�X�N �����i�����I�Ɏ����j """
        # ����Ń}�b�`�����ߖT�̈�ȊO�Ƀ}�X�N�������A�������x���シ��
        # ���������G�ʒu�����I�ɕω����Ȃ��O��
        pass

    def calc_detect_location(self, loc_max, master, location="center"):
        """ �⑫���W ���Z """
        height, width, channel = master.shape
        # �������W ���Z
        if location == "center":
            coord = (loc_max[0] + width / 2, loc_max[1] + height / 2)
        # �E�����W ���Z
        elif location == "tail":
            coord = (loc_max[0] + width, loc_max[1] + height)
        return coord, height, width

    def show_detect_area(self, loc_max, frame, master):
        """ �⑫�͈� ���Z """
        # �������W ���Z
        coord, height, width\
            = self.calc_detect_location(loc_max, master, "center")
        left_up = (loc_max[0], loc_max[1])
        right_bottom = (loc_max[0] + width, loc_max[1] + height)
        detect = frame[loc_max[1]:loc_max[1] + height,
                        loc_max[0]:loc_max[0] + width].copy()
        return detect, left_up, right_bottom


class ImageProcessing:
    """ ����擾 �N���X """
    def __init__(self):
        self.ci = ConvertImage()
        self.tm = Tplmatching()
        self.ciadp = self.ci.adaptive_threashold
        self.cidca = self.ci.discriminantanalyse
        self.cibiz = self.ci.binarize
        self.cinor = self.ci.normalize

        # ���� �擾
        self.cap = cv2.VideoCapture(0)

        # ���������
        self.text2 = "End: Long press \"e\" key"
        self.text3 = "Mastering: Long press \"m\" key"

        # �}�b�`����l
        self.judge = 0.70
        # ���K���i�����\���j�̋����x
        self.highlight = 4
        # OK�Ɣ��肷�鎞��
        self.ok_time = 2
        self.ok_count = 0

    def init_get_camera_image(self, name):
        """ �J�������瓮��擾 """
        # �J�����L���v�`�����̃C�j�V�����C�Y �f�B���C����
        time.sleep(0.1)
        if not self.cap.isOpened():
            print("Can not connect camera...")
            terminate()
            # �g���b�N�o�[ ��`(�ł��Ȃ�)�I�I�I# {{{
            #        name_bar = "Max threshold"
            #        print(thresh_max)
            # # �g���b�N�o�[ ����
            #        def set_parameter(value):
            #            thresh_max = cv2.getTrackbarPos(name_bar, name_window)
            #            thresh_max = cv2.setTrackbarPos(name_bar, name_window)
            #        cv2.createTrackbar(name_bar, name_window,
            #           0, 255, self.thresh_max)
            #        name_window = "Adaptive Threashold cap"
            # }}}
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

    def run(self, name, search, extension=".png", dir_master="MasterImage"):
        """ ����擾 �����i���C�����[�`���j """  # {{{
        print("-" * 50)
        print("START TEMPLATE MATCHING".center(print_col, " "))
        print("-" * 50)
        print("")
        print(" SEARCH MASTER MODE ".center(print_col, "*"))
        print("")
        cwd = os.getcwd()
        path_master = cwd + "\\" + dir_master
        print("Master directory:")
        print(path_master.rjust(print_col, " "))

        # �ŏI�}�Ԃ̃}�X�^�[�摜 �擾
        # TODO: �����T���̎��͂�����" sda "���C�e���[�g�����I�I�I
        sda = sd.SaveData(search, path_master)
        set_name, name_master, match_flag = sda.get_name_max(extension)

        print(" RETURN TEMPLATE MATCHING ".center(print_col, "*"))
        print("")

        # �}�X�^�[�摜�L�� ����
        if match_flag is False:
            print("No match master")
            print("Go get master mode(no match master case)")
            print("")

            self.get_master(search, extension, path_master)
            set_name, name_master, match_flag = sda.get_name_max(extension)

            print("Get master name: " + str(name_master))
            print("")

        else:
            print("Match master name: " + str(name_master))
            print("Match master extension: " + str(extension))
            print("")
        # TODO: �C�e���[�g�����\�� �����܂ŁI�I�I

        self.init_get_camera_image(name)

        # !!!: ��������
        count = 0
        while True:
            if count < 1:
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
        # !!!: �ȏ�܂ł�class�ɂ�������"while"����"frame"��
        # "while"�O�ɏo���Ȃ��̂Œf�O�I�I�I
        # ���֐��ɂ���(�ł��Ȃ������I�I�I)�H�H�H
            # }}}

            # �}�X�^�[�摜�̌����ƃZ�b�g �\��
            print("")
            print("Master name: "\
                    + str(name_master) + str(extension) + "\r\n")

            master = str(path_master) + ".\\"\
                    + str(name_master) + str(extension)
            master = cv2.imread(str(master), cv2.IMREAD_COLOR)

            # �e���v���[�g�}�b�`���O �C�e���[�g����

            # TODO: �����T���̎��͂����̃^�v���Ƀ}�X�^�[������
            # �]���p �������X�g
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

                # �e���v���[�g�}�b�`���O ����
                match, value_min, value_max, loc_min, loc_max\
                        = self.tm.tplmatch(frame_eval, master_eval)

                # �⑫�͈� ���K���i�⑫�����\���p�j
                norm = self.cinor(match)

                # �}�b�`���O�̈� �g��������
                detect, left_up, right_bottom\
                        = self.tm.show_detect_area(loc_max, frame, master)
                if method[1] is not None:
                    detect = method[1](detect)

                # �}�b�` ����
                trim = tm.Trim(frame_eval, None, None, None, 1)
                if value_max > self.judge:

                    # TODO: *�b��OK�ŉ�ʕ\���I�I�I
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

                            # ���茋�� �\��
                            trim.write_text("OK", (0, "height"), 2,
                                            "white", "green", 5, 4, (0, 10))
                            # ���o�ʒu ��`�\��
                            trim.draw_rectangle(left_up, right_bottom,
                                                "white", "green")
                            # �ގ��x �\��
                            similarity = round(value_max * 100, 1)
                            trim.write_text(str(similarity) + "%",
                                            (right_bottom[0], "height"),
                                            scale=0.6,
                                            color_out="white",
                                            color_in="green",
                                            thickness_out=3,
                                            thickness_in=2,
                                            gap=(0, right_bottom[1] + 5))

                        # TODO: OK�� �o�́I�I�I

                        # TODO: ���O �o�́I�I�I

                else:
                    self.ok_count = 0
                    self.ok_start = 0
                    # ���茋�� �\��
                    trim.write_text("NG", (0, "height"), 2,
                                    "white", "red", 5, 4, (0, 10))

                    # TODO: NG�� �o�́I�I�I

                    # TODO: ���O �o�́I�I�I

                # �]������ ��ʕ\��
                self.ci.display(str(method[0] + " frame"), frame_eval)
                self.ci.display(str(method[0] + " master"), master_eval)
                self.ci.display("Detected " + str(method[0]), detect, 1)
                self.ci.display("Normalize " + str(method[0]),
                                norm ** self.highlight, 1)  # frame���master���k��

                # ������@������ �\���ʒu �擾
                text_offset = 10
                baseline = frame.shape[0] - text_offset
                origin = 1, baseline

                # ������@������ �\��
                operation = frame
                trim = tm.Trim(operation, None, None, None, 1)
                text_height = trim.write_text(self.text2, origin)
                trim.write_text(self.text3,\
                        (origin[0], origin[1] - text_offset - text_height[1]))

                # ���C����� �\��
                self.ci.display(name, operation)
                # import pdb; pdb.set_trace()

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

            # "m"�L�[���� �}�X�^�[�摜�擾���[�h �J��
            if cv2.waitKey(33) == ord("m"):
                print("")
                print("Input key \"m\"")
                print("Go get master mode")
                print("")
                time.sleep(0.5)
                # TODO: �����T���̎��͂�����" sda "���C�e���[�g�����I�I�I
                self.get_master(search, extension, path_master)
                set_name, name_master, match_flag = sda.get_name_max(extension)
                # TODO: �C�e���[�g�����\�� �����܂ŁI�I�I
                cv2.destroyAllWindows()
                print("Get master name: " + str(name_master))

            # ���̏I�������I�I�I
            # "q"�L�[���� �I������
            if cv2.waitKey(33) == ord("e"):
                print("")
                print("Input key \"e\"")
                print(" END PROCESS ".center(print_col, "*"))
                break

    def get_master(self, search, extension, path):
        """ �}�X�^�[�摜 �Ǎ��� """
        name = "Get master image"
        text2 = "Quit: Long press \"q\" key"
        text3 = "Trimming: Long press \"t\" key"

        print("")
        print(" START GET MASTER MODE ".center(print_col, "*"))
        print("Search master name: " + str(search))
        print("Master image name: " + str(search))

        self.init_get_camera_image(name)

        count = 0
        while True:
            if count < 1:
                print("Initial delay")
                time.sleep(0.1)
            get_flag, frame = self.cap.read()
            get_flag_draw, frame_draw = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            # ������@������ �\���ʒu �擾
            text_offset = 10
            baseline = frame.shape[0] - text_offset
            origin = 1, baseline

            # ������@������ �\��
            trim = tm.Trim(frame_draw, search, extension, path, 1)
            text_height = trim.write_text(text2, origin)
            trim.write_text(text3,\
                    (origin[0], origin[1] - text_offset - text_height[1]))

            self.ci.display(name, frame_draw)
            print("Master captcha")
            count += 1

            # "t"�L�[���� �}�X�^�[�摜�擾���[�h �J��
            if cv2.waitKey(33) == ord("t"):
                print("")
                print("Input key \"t\"")
                print("Go master mode")
                time.sleep(1)
                img = "master_source{}".format(extension)
                cv2.imwrite(img, frame)
                trim = tm.Trim(img, search, extension, path)
                trim.trim()

            # "q"�L�[���� �I������
            if cv2.waitKey(33) == ord("q"):
                print("")
                print("Input key \"q\"")
                time.sleep(1)
                print(" END GET MASTER MODE ".center(print_col, "*"))
                print("")
                # import pdb; pdb.set_trace()
                break

    def check_get_flag(self, flag):
        """ ����擾�~�X�� �X�L�b�v���� """  # {{{
        if flag is False:
            print("Can not get end flag")
            return False
            # }}}

    def check_get_frame(self, frame):
        """ ���[�v �I������ """  # {{{
        if frame is None:
            print("Can not get video frame")
            return False
            # }}}


def main():
    # vim�e�X�g�p�e�ϐ� ��`# {{{
    # �C�j�V������� �o��
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
    print("��" * int(print_col / 2))
    print("START MAIN".center(print_col, " "))
    print("��" * int(print_col / 2))
    print("")
    # import pdb; pdb.set_trace()

    path = "D:\\OneDrive\\Biz\\Python\\ImageProcessing"
    smpl_pic = "D:\\OneDrive\\Biz\\Python\\ImageProcessing\\tpl_1.png"
    smpl_pic2 = "D:\\OneDrive\\Biz\\Python\\ImageProcessing\\tpl_2.png"
# }}}

    # �e���v���[�g�}�b�`���O �e�X�g# {{{
    cip = ImageProcessing()
    cip.run("Raw capture", "masterImage")
    print("Image processing end...")
    # }}}

#     # �Î~��擾 �e�X�g# {{{
#     gim = GetImage(smpl_pic)
#     gim2 = GetImage("tpl_3.png")
#     # gim.diplay("Tes1", 0, 0)
#     gim2.display("Tes2", 0, 0)
#     print("Main loop end...")
# # }}}

# # ����擾 �e�X�g# {{{
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
#     # ���̏o�͕ێ������I�I�I
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#     image = cv2.imread("tpl_2.png")
#     ci = ConvertImage()
#     ci.adaptive_threashold(image, "Adaptive Threashold", 0)
#     print("Sudah cap")
# # }}}

    # # �h�L�������g�X�g�����O# {{{
    # print(GetImage.__doc__)
    # print(help(__name__))
    # }}}

if __name__ == '__main__':
    main()
