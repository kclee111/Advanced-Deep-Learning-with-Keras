import os
import sys
import inspect
from typing import Callable, Union
import numpy as np
import numpy.typing as npt
import pandas as pd
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


if os.name == "nt":
    try:
        # 폰트 경로 설정
        font_path = "C:\\Users\\kclee\\AppData\\Local\\Microsoft\\Windows\\Fonts"
        # 폰트 이름 가져오기
        font_files = matplotlib.font_manager.findSystemFonts(fontpaths=font_path)
        for fpath in font_files:
            matplotlib.font_manager.fontManager.addfont(fpath)

        # 폰트 설정
        matplotlib.rcParams["font.family"] = ["DejaVu Sans", "NanumBarunGothic"]
        print(f"Matplotlib: Windows 나눔바른고딕 폰트로 설정되었습니다.")

    except:
        plt.rcParams["font.family"] = ["DejaVu Sans", "Malgun Gothic"]
        print(f"Matplotlib: 맑은고딕 폰트로 설정되었습니다.")
else:
    font_files = matplotlib.font_manager.findSystemFonts(fontpaths="/usr/share/fonts/truetype")
    for fpath in font_files:
        matplotlib.font_manager.fontManager.addfont(fpath)
    fm = matplotlib.font_manager.FontManager()
    if "NanumBarunGothic" in fm.get_font_names():
        matplotlib.rcParams["font.family"] = ["DejaVu Sans", "NanumBarunGothic"]  # 리눅스 환경에서 나눔바른고딕 폰트가 있으면 설정
        print(f"Matplotlib: Ubuntu 나눔바른고딕 폰트로 설정되었습니다.")
    else:
        print(f"In Ubuntu Matplotlib 그래프 객체에서 한글이 지원되지 않습니다.")

matplotlib.rcParams["axes.unicode_minus"] = False

local_folder = Path("datatest")
github_url = "https://raw.githubusercontent.com/dglee6257/Dataprocessing/main/datatest/"

def read_csv(file, **kwargs) -> pd.DataFrame:
    """read csv file from local folder if exists, otherwise from github folder"""
    try:
        df = pd.read_csv(local_folder / file, **kwargs)
    except FileNotFoundError:
        df = pd.read_csv(github_url + file, **kwargs)
    return df


def read_excel(file, **kwargs) -> pd.DataFrame:
    """read excel file from local folder if exists, otherwise from github folder"""
    try:
        df = pd.read_excel(local_folder / file, **kwargs)
    except FileNotFoundError:
        df = pd.read_excel(github_url + file, **kwargs)
    return df

import json
class dotdict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = attrdict() or d = attrdict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        return json.dumps(self, indent=2, default=str)

    def __getitem__(self, index):
        if isinstance(index, (int, slice)):
            items = list(self.values())
            return items[index]
        else:
            return dict.__getitem__(self, index)

    def tolist(self):
        return list(self.keys())

    to_list = tolist

    def filter(self, key_filter: Union[str, Callable]):
        if callable(key_filter):
            return dotdict([(k, v) for k, v in self.items() if key_filter(k)])
        elif isinstance(key_filter, str):
            return dotdict([(k, v) for k, v in self.items()  if key_filter in str(k)])

    def isupper(self):
        return dotdict([(k, v) for k, v in self.items() if k[0].isupper()])

    def islower(self):
        return dotdict([(k, v) for k, v in self.items() if k[0].islower()])

    def isin(self, keys):
        if isinstance(keys, dict):
            keys = list(keys.keys())
        else:
            keys = list(keys)
        return dotdict([(k, v) for k, v in self.items() if k in keys])

    def isnotin(self, keys):
        if isinstance(keys, dict):
            keys = list(keys.keys())
        else:
            keys = list(keys)
        return dotdict([(k, v) for k, v in self.items() if not k in keys])

def attr(obj):
    """Returns obj's state_types, callable_signatures, state_values, and callables_bounded"""
    all_attr = {}
    for attribute in dir(obj):
        if not attribute.startswith("_"):
            try:
                all_attr[attribute] = getattr(obj, attribute)
            except Exception as e:
                continue

    methods = dict([(k, v) for k, v in all_attr.items() if callable(v)])

    signatures = {}
    for k, v in all_attr.items():
        if callable(v):
            try:
                signatures[k] = inspect.signature(v)  # may occur ValueError
            except Exception as e:
                signatures[k] = "No signature available for built-in method"

    state_keys = sorted(list(set(all_attr.keys()) - set(methods.keys())))
    state_types = dict([(k, type(getattr(obj, k))) for k in state_keys])
    state_values = dict([(k, getattr(obj, k)) for k in state_keys])

    return dotdict(
        a=dotdict(state_types),
        b=dotdict(signatures),
        c=dotdict(state_values),
        d=dotdict(methods),
    )

# insert row
def insert_row(df: pd.DataFrame, row) -> pd.DataFrame:
    df[len(df)] = row
    return df.reset_index(drop=True)

# import pymc as pm
# import pymc.math as pmath
# import pytensor.tensor as tt
# import xarray as xr

pmstack = lambda x: x.stack(sample=("chain", "draw")).transpose("sample", ...)
def kv(obj):
    for k, v in obj.items():
        print(f"{k}:\n{v}")
        print()

def itemsview(obj: dict):
    try:
        for k, v in obj.items():
            print(f"{k} -> {v}")
    except AttributeError:
        print(f"obj is not dict -> {type(obj)}")
