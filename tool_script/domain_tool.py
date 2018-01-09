# -*- coding:utf-8 -*-

INTERNATIONAL_POSTFIX = {
    ".com",
    ".edu",
    ".gov",
    ".int",
    ".mil",
    ".net",
    ".org",
    ".biz",
    ".info",
    ".pro",
    ".name",
    ".museum",
    ".coop",
    ".aero",
    ".xxx",
    ".idv"
}

from enum import Enum, unique
from lxml import etree
from StringIO import StringIO
import requests
import re


def judge_postfix_type(domain):
    item_list = domain.split('.')
    temp_list = [] 
    for item in item_list:
        if item:
            temp_list.append(item)

    if len(temp_list) <= 1:
        raise Exception("错误域名")

    pf = temp_list[-1]
    pf = '.' + pf
    if pf in INTERNATIONAL_POSTFIX:
        return "国际域名"
    if pf == ".cn":
        return "中国大陆域名"
    return  "其他域名"


def is_en_word(word):
    url = 'http://www.iciba.com/' + word
    res = requests.get(url)
    if res.status_code == 200:
        return True
    return False


def length_weight(domain):
    temp_list = domain.split('.')
    # 主域名
    main_domain = temp_list[-2] 
    l = len(main_domain)
    if l <= 0:
        return 0
    base = 1
    if l <= 1:
        return 1000
    if l <= 2:
        return 100
    if l <= 3:
        base = 10 
    
    # 尝试看看主域名中是否有英文单词
    # 有英文单词的域名更容易记忆，因此价值更高
    if is_en_word(main_domain):
        base = base * 5

    return base

def extract_count(value):
    #1
    #37,625
    #24,900
    #1亿8448万
    #100,000,000
    if ',' in value:

    pass

def evaluate(domain):
    pass

def itself_value(domain):
    total = 0
    tp = judge_postfix_type(domain)
    tp_weight = 0
    if tp == '国际域名':
        tp_weight = 5
    elif tp == '中国大陆域名':
        tp_weight = 3
    else:
        tp_weight = 2 

    total = 10 * tp_weight * length_weight(domain) 
    return total

def get_baidu_include(domain):
    url = 'http://www.baidu.com/s?wd=site:' + domain
    res = requests.get(url)
    #print t.text
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(res.text), parser)

    item_list = tree.xpath('//*[@id="1"]/div/div[1]/div/p[3]/span/b')
    value = '0'
    # 1,493
    # 1亿0000万 
    # 2690000
    # 9590
    # 1亿8448万
    for item in item_list:
        value = item.text

    item_list = tree.xpath('//*[@id="content_left"]/div[1]/div/p[1]/b')
    for item in item_list:
        value = item.text

    print value

def get_so_include(domain):
    url = 'https://www.so.com/s?q=site:' + domain 
    res = requests.get(url)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(res.text), parser)
    item_list = tree.xpath('//*[@id="main"]/p')
    value = '0'
    for item in item_list:
        value = item.text

    item_list = tree.xpath('//*[@id="main"]/div/ul/li/p[3]/text()')
    for item in item_list:
        value = item
    
    start = value.find(u'约')
    start += 1
    end = value.find(u'个')
    print value[start: end]

def added_value(domain):
    # 获取google
    pass



if __name__ == "__main__":
    domain1 = 'baidu.com'
    domain2 = "xiaorui.cc"
    domain3 = "umeng.com"
    domain4 = "tudou.com"
    #domain4 = ".umeng"
    #get_baidu_include(domain1)
    #get_baidu_include(domain2)
    #get_so_include(domain2)
    #get_baidu_include(domain3)
    #get_so_include(domain3)
    #get_baidu_include(domain4)
    #get_so_include(domain4)
    #get_baidu_include(domain3)


    #print itself_value(domain1)
    #print itself_value(domain2)
    #print itself_value(domain3)
    #print itself_value(domain4)
    #length_weight(domain1)
    #length_weight(domain2)
    #length_weight(domain3)
    #length_weight(domain4)
    #print judge_postfix_type(domain1)
    #print judge_postfix_type(domain2)
    #print judge_postfix_type(domain3)
    #print judge_postfix_type(domain4)


