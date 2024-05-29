import re

# 定义一个正则表达式来匹配中文大写金额
pattern = r'[\u4e00-\u9fa5]+'

# 给定的字符串
string = "xyz贰拾肆圆零柒分 ¥24.07"

# 使用正则表达式找到匹配项
chinese_amount = re.findall(pattern, string)
rs= chinese_amount[0] if chinese_amount else "未找到匹配项"

print(rs)