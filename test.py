def chinese_to_numerals(chinese_str):
    chinese_numerals = {'零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4,
                        '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9}
    chinese_units = {'圆': 1, '角': 0.1, '分': 0.01}

    num = 0
    temp = 0  # 临时存储中间结果

    for char in chinese_str:
        if char in chinese_units:
            unit = chinese_units[char]
            num += temp * unit
            temp = 0
        elif char in chinese_numerals:
            temp += chinese_numerals[char]
        elif char == '拾':
            temp *= 10
        elif char == '佰':
            temp *= 100
        elif char == '仟':
            temp *= 1000
        elif char == '万':
            temp *= 10000
        elif char == '亿':
            temp *= 100000000

    return num


# 测试
chinese_amount = '贰拾肆圆零柒分'
print(chinese_to_numerals(chinese_amount))


# 增加更多测试用例
additional_test_data = [
    '壹圆壹角壹分',
    '壹仟圆',
    '壹佰万圆',
    '壹佰亿圆',
    '壹佰亿零壹圆',
    '壹仟零壹圆',
    '壹拾圆壹角',
    '贰佰圆贰拾分',
    '叁仟伍佰陆拾柒圆捌角零分',
    '肆佰零伍圆'
]

additional_results = [(data, chinese_to_numerals(data)) for data in additional_test_data]

print(additional_results)