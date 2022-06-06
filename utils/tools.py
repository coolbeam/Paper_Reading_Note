import cv2
import numpy as np
import os
import pickle
import argparse
import collections
import random
from shutil import rmtree
import time
import array
import warnings
import shutil
import re
from collections import Iterable


class tools():
    class abstract_config():
        _update_ignore_keys=[]
        @classmethod
        def _check_length_of_file_name(cls, file_name):
            if len(file_name) >= 255:
                return False
            else:
                return True

        @classmethod
        def _check_length_of_file_path(cls, filepath):
            if len(filepath) >= 4096:
                return False
            else:
                return True

        @property
        def to_dict(self):
            def dict_class(obj):
                temp = {}
                k = dir(obj)
                for name in k:
                    if not name.startswith('_') and name != 'to_dict':
                        value = getattr(obj, name)
                        if callable(value):
                            pass
                        else:
                            temp[name] = value
                return temp

            s_dict = dict_class(self)
            return s_dict

        @property
        def _key_list(self):
            k_list = list(self.to_dict.keys())
            return k_list

        def update(self, data: dict):

            t_key = list(data.keys())
            for i in self._key_list:
                if i in t_key and i not in self._update_ignore_keys:
                    setattr(self, i, data[i])
                    # print('set param ====  %s:   %s' % (i, data[i]))

        def __contains__(self, item):
            '''  use to check something in config '''
            if item in self._key_list:
                return True
            else:
                return False

        def print_defaut_dict(self):
            d = self.to_dict
            l = self._key_list
            l = sorted(l)
            for i in l:
                value = d[i]
                if type(value) == str:
                    temp = "'%s'" % value
                else:
                    temp = value
                print("'%s':%s," % (i, temp))

        @classmethod
        def __demo(cls):
            class temp(tools.abstract_config):
                def __init__(self, **kwargs):
                    self.if_gpu = True
                    self.eval_batch_size = 1
                    self.eval_name = 'flyingchairs'
                    self.eval_datatype = 'nori'  # or base
                    self.if_print_process = False

                    self.update(kwargs)

            a = temp(eval_batch_size=8, eval_name='flyingchairs', eval_datatype='nori', if_print_process=False)

    # 研究一下图像加字体展示结果
    class Text_img():
        def __init__(self, **kwargs):
            self.font = 'simplex'
            self.my_font_type = 'black_white'
            self.__update(kwargs)
            self.font_ls = {
                'simplex': cv2.FONT_HERSHEY_SIMPLEX,
                'plain': cv2.FONT_HERSHEY_PLAIN,
                'complex': cv2.FONT_HERSHEY_COMPLEX,
                'trplex': cv2.FONT_HERSHEY_TRIPLEX,
                # 'complex_small': cv2.FONT_HERSHEY_COMPLEX_SMALL,
                'italic': cv2.FONT_ITALIC,
            }
            self.my_font_type_ls = {
                'black_white': self._black_white,
            }
            self.show_func = self.my_font_type_ls[self.my_font_type]

        def __update(self, data: dict):
            def dict_class(obj):
                temp = {}
                k = dir(obj)
                for name in k:
                    if not name.startswith('_'):
                        value = getattr(obj, name)
                        if callable(value):
                            pass
                        else:
                            temp[name] = value
                return temp

            s_dict = dict_class(self)
            k_list = list(s_dict.keys())
            t_key = list(data.keys())
            for i in k_list:
                if i in t_key:
                    setattr(self, i, data[i])
                    # print('set param ====  %s:   %s' % (i, data[i]))

        def _black_white(self, img, text, scale, row=0):
            # params
            color_1 = (10, 10, 10)
            thick_1 = 5
            color_2 = (255, 255, 255)
            thick_2 = 2

            # get position: Bottom-left
            t_w, t_h, t_inter = self._check_text_size(text=text, scale=scale, thick=thick_1)
            pw = t_inter
            ph = t_h + t_inter + row * (t_h + t_inter)

            # put text
            img_ = img.copy()
            img_ = cv2.putText(img_, text, (pw, ph), fontFace=self.font_ls[self.font], fontScale=scale, color=color_1, thickness=thick_1)
            img_ = cv2.putText(img_, text, (pw, ph), fontFace=self.font_ls[self.font], fontScale=scale, color=color_2, thickness=thick_2)
            return img_

        def _check_text_size(self, text: str, scale=1, thick=1):
            textSize, baseline = cv2.getTextSize(text, self.font_ls[self.font], scale, thick)
            twidth, theight = textSize
            return twidth, theight, baseline // 2

        def put_text(self, img, text=None, scale=1):
            if text is not None:
                if type(text) == str:
                    img = self.show_func(img, text, scale, 0)
                elif isinstance(text, Iterable):
                    for i, t in enumerate(text):
                        img = self.show_func(img, t, scale, i)
            return img

        def draw_cross(self, img, point_wh, cross_length=5, color=(0, 0, 255)):  #
            thick = cross_length // 2
            new_img = img.copy()
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1]), (point_wh[0] + cross_length, point_wh[1]), color, thick)
            new_img = cv2.line(new_img, (point_wh[0], point_wh[1] - cross_length), (point_wh[0], point_wh[1] + cross_length), color, thick)
            return new_img

        def draw_cross_black_white(self, img, point_wh, cross_length=5):  #
            if cross_length <= 5:
                cross_length = 5
            thick = cross_length // 2
            new_img = img.copy()
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1]), (point_wh[0] + cross_length, point_wh[1]), (0, 0, 0), thick)
            new_img = cv2.line(new_img, (point_wh[0], point_wh[1] - cross_length), (point_wh[0], point_wh[1] + cross_length), (0, 0, 0), thick)
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1]), (point_wh[0] + cross_length, point_wh[1]), (250, 250, 250), thick // 2)
            new_img = cv2.line(new_img, (point_wh[0], point_wh[1] - cross_length), (point_wh[0], point_wh[1] + cross_length), (250, 250, 250), thick // 2)
            return new_img

        def draw_x(self, img, point_wh, cross_length=5, color=(0, 0, 255)):
            thick = cross_length // 2
            new_img = img.copy()
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1] - cross_length), (point_wh[0] + cross_length, point_wh[1] + cross_length), color, thick)
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1] + cross_length), (point_wh[0] + cross_length, point_wh[1] - cross_length), color, thick)
            return new_img

        def draw_x_black_white(self, img, point_wh, cross_length=5):
            if cross_length <= 5:
                cross_length = 5
            thick = cross_length // 2
            new_img = img.copy()
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1] - cross_length), (point_wh[0] + cross_length, point_wh[1] + cross_length), (0, 0, 0), thick)
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1] + cross_length), (point_wh[0] + cross_length, point_wh[1] - cross_length), (0, 0, 0), thick)
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1] - cross_length), (point_wh[0] + cross_length, point_wh[1] + cross_length), (250, 250, 250), thick // 2)
            new_img = cv2.line(new_img, (point_wh[0] - cross_length, point_wh[1] + cross_length), (point_wh[0] + cross_length, point_wh[1] - cross_length), (250, 250, 250), thick // 2)
            return new_img

        def show_img_dict(self, **kwargs):
            for i in kwargs.keys():
                img = self.put_text(kwargs[i], text=i)
                cv2.imshow(i, img)
            cv2.waitKey()

        def demo(self):
            im = np.ones((500, 500, 3), dtype='uint8') * 50
            imshow = self.put_text(im, text=list('demo show sample text'.split(' ')), scale=1)
            cv2.imshow('im', imshow)
            cv2.waitKey()

    class npz_saver():

        @classmethod
        def save_npz(cls, files, npz_save_path):
            np.savez(npz_save_path, files=[files, 0])

        @classmethod
        def load_npz(cls, npz_save_path):
            with np.load(npz_save_path) as fin:
                files = fin['files']
                files = list(files)
                return files[0]

    class pickle_saver():

        @classmethod
        def save_pickle(cls, files, file_path):
            with open(file_path, 'wb') as data:
                pickle.dump(files, data)

        @classmethod
        def load_picke(cls, file_path):
            with open(file_path, 'rb') as data:
                data = pickle.load(data)
            return data

    class txt_read_write():
        @classmethod
        def read(cls, path):
            with open(path, "r") as f:
                data = f.readlines()
            return data

        @classmethod
        def write(cls, path, data_ls):
            file_write_obj = open(path, 'a')
            for i in data_ls:
                file_write_obj.writelines(i)
            file_write_obj.close()

        @classmethod
        def demo(cls):
            txt_path = r'E:\research\unsupervised_optical_flow\projects\Ric-master\Ric-master\data\MPI-Sintel\frame_0001_match.txt'
            data = tools.txt_read_write.read(txt_path)
            print(' ')
            write_txt_path = txt_path = r'E:\research\unsupervised_optical_flow\projects\Ric-master\Ric-master\data\MPI-Sintel\temp.txt'
            tools.txt_read_write.write(write_txt_path, data[:10])
            print(' ')

    @classmethod
    def check_dir(cls, path):
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def clear(cls):
        os.system("clear")  # 清屏

    @classmethod
    def random_flag(cls, threshold_0_1=0.5):
        a = random.random() < threshold_0_1
        return a
