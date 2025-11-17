import base64


def base64_encode(original_string):
    """
    将字符串或字节数据编码为Base64格式的字符串。

    参数:
        original_string: 要编码的原始字符串。

    返回:
        str: Base64编码后的字符串。如果编码失败，返回None。
    """
    try:
        # 确保输入转换为字节
        if isinstance(original_string, str):
            original_bytes = original_string.encode('utf-8')
        else:
            original_bytes = original_string

        # 进行Base64编码，并转换为ASCII字符串以便使用
        encoded_bytes = base64.b64encode(original_bytes)
        encoded_string = encoded_bytes.decode('ascii')
        return encoded_string
    except Exception as e:
        print(f"编码过程中出现错误: {e}")
        return None


def base64_decode(encoded_string):
    """
    将Base64格式的字符串解码为原始字符串。

    参数:
        encoded_string: Base64编码的字符串。

    返回:
        str: 解码后的原始字符串。如果解码失败，返回None。
    """
    try:
        # 处理可能缺失的填充符'='，确保长度是4的倍数
        encoded_string = encoded_string.strip()  # 去除首尾空格
        missing_padding = len(encoded_string) % 4
        if missing_padding != 0:
            encoded_string += '=' * (4 - missing_padding)

        # 将字符串转换为字节并进行解码
        encoded_bytes = encoded_string.encode('ascii')
        decoded_bytes = base64.b64decode(encoded_bytes)

        # 尝试将解码后的字节转换回字符串
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print(f"解码过程中出现错误: {e}")
        return None


