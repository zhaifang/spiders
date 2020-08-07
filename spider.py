# -*- coding:utf-8 -*-

import fire
import plug_ins

import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    fire.Fire(*(getattr(plug_ins, i) for i in plug_ins.__all__))