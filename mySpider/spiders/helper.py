import re

def is_ad(s): #判断楼层是否为广告
    ad = s.xpath(u".//span[contains(text(), '广告')]")
    # 广告楼层中间有个span含有广告俩字
    return ad

def strip_blank(s): #按个人喜好去掉空白字符
    s = re.sub(r'\n[ \t]+\n', '\n', s)
    s = re.sub(r'  +', ' ', s) #去掉多余的空格
    s = re.sub(r'\n\n\n+', '\n\n', s) #去掉过多的连续换行
    return s.strip()