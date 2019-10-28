# -*- coding: utf-8 -*-
import pypinyin
from pypinyin import pinyin
def get_pingyin(ss):
    '''
        获取字符串的拼音首字母
    :param ss: 必须是unicode类型
    :return:
    '''
    res = pinyin(ss, style=pypinyin.FIRST_LETTER)
    ll = []
    for item in res:
        ll.append(item[0])
    return ''.join(ll)
