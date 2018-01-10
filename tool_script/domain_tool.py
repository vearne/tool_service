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
    if isinstance(value, unicode):
        value = value.encode('utf-8')

    if ',' in value:
        item_list = value.split(',')
        x = ''.join(item_list)
        return int(x)
    
    res = re.match(r'(\d+)亿(\d+)万', value)
    if res:
        v1 = res.group(1)
        v2 = res.group(2)
        return int(v1) * 1000000000 + int(v2) * 10000 

    return int(value)


def get_comment(value):
    if value <= 1000:
        return u"别看了，就值这么多了😂"
    elif value <= 10000:
        return u"了不起，广阔天地，大有可为😑" 
    elif value <= 1000000:
        return u"价值不菲，奇货可居啊!😋" 
    else:
        return u"土豪，咱们做朋友吧!!!😍"


def evaluate(domain):
    dd = {
        "itself_value": 0, 
        "added_value": 0, 
        "total_value": 0,
        "comment": ""
    }
    try:
        iv = itself_value(domain)
        av = added_value(domain)
        dd['itself_value'] = iv
        dd['added_value'] = av
        dd['total_value'] = av + iv
        dd['comment'] = get_comment(av+iv)
        return dd
    except:
        dd['comment'] = '错误域名' 
        return dd 


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
    for item in item_list:
        value = item.text
        
    # 找到相关结果数约2个
    item_list = tree.xpath('//*[@id="content_left"]/div[1]/div/p[1]/b')
    for item in item_list:
        temp = item.text
        start = temp.find(u'约')
        end = temp.find(u'个')
        value = temp[start + 1:end]

    return extract_count(value.strip())

def get_so_include(domain):
    url = 'https://www.so.com/s?q=site:' + domain 
    res = requests.get(url)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(res.text), parser)
    item_list = tree.xpath('//*[@id="main"]/p')
    value = '0'
    # 
    for item in item_list:
        temp = item.text
        start = temp.find(u'约')
        start += 1
        end = temp.find(u'个')
        value = temp[start: end].strip()

    item_list = tree.xpath('//*[@id="main"]/div/ul/li/p[3]/text()')
    for item in item_list:
        temp = item
        start = temp.find(u'约')
        start += 1
        end = temp.find(u'个')
        value = temp[start: end].strip()

    return extract_count(value)

def added_value(domain):
    # 获取baidu
    baidu_count = get_baidu_include(domain)
    print "baidu include", baidu_count
    # 获取so
    so_count = get_so_include(domain)
    print "so include", so_count
    
    # 增加一定的随机因素
    base = hash(domain) % 9 * 0.1 + 9
    print 'base', base
    
    return base * (baidu_count + so_count)


if __name__ == "__main__":
    domain1 = 'vearne.cc'
    domain2 = "xiaorui.cc"
    domain3 = "umeng.com"
    domain4 = "tudou.com"
    domain5 = "abcdefxxx"
    
    #print added_value(domain1)
    #print added_value(domain2)
    #print added_value(domain3)
    #print evaluate(domain1)
    print evaluate(domain1)
    print evaluate(domain2)
    print evaluate(domain3)
    print evaluate(domain4)
    print evaluate(domain5)


