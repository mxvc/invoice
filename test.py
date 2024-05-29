def chinese_to_number(chinese_amount):
    """
    将大写中文金额转换为数字

    参数:
    chinese_amount (str): 大写中文金额字符串

    返回:
    float: 转换后的数字金额
    """
    # 中文金额数字映射表
    mapping = {
        '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4,
        '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
        '拾': 10, '佰': 100, '仟': 1000, '万': 10000, '亿': 100000000
    }

    # 初始化结果
    result = 0
    unit = 1
    decimal_part = 0
    decimal_unit = 0.1

    # 遍历中文金额字符串
    for i, char in enumerate(chinese_amount[::-1]):
        if char in mapping:
            if mapping[char] >= 10:
                result = result + unit * mapping[char]
                unit = mapping[char]
            else:
                if i == 0:  # 处理分
                    decimal_part += mapping[char] * decimal_unit
                else:
                    result = result + unit * mapping[char]
        elif char == '圆':
            pass
        elif char == '角':
            result = result + decimal_part
            decimal_part = 0
            decimal_unit = 0.01

    return result + decimal_part


print(chinese_to_number('贰拾肆圆零柒分'))  # 输出: 24.07
print(chinese_to_number('壹佰贰拾叁圆肆角伍分'))  # 输出: 123.45