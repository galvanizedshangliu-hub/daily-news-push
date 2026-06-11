"""
Server酱消息发送模块
通过Server酱发送消息到微信公众号
"""

import requests


def send_to_serverchan(title, content, sendkey):
    """
    通过Server酱发送消息

    Args:
        title: 消息标题（必填，不超过256字）
        content: 消息内容（支持Markdown）
        sendkey: Server酱的SendKey

    Returns:
        发送结果字典
    """
    try:
        url = f"https://sctapi.ftqq.com/{sendkey}.send"

        data = {
            "title": title,
            "desp": content
        }

        response = requests.post(url, data=data)
        result = response.json()

        if result.get("code") == 0:
            print("Server酱消息发送成功")
            print(f"  消息ID: {result.get('data', {}).get('pushid')}")
        else:
            print(f"Server酱消息发送失败: {result}")

        return result

    except Exception as e:
        print(f"Server酱发送异常: {e}")
        return {"code": -1, "message": str(e)}


if __name__ == "__main__":
    # 测试
    test_sendkey = "your_sendkey_here"
    test_title = "测试消息"
    test_content = "# 测试\n\n这是一条测试消息"

    print("Server酱模块加载成功")
    print("实际使用时请提供真实的SendKey")
