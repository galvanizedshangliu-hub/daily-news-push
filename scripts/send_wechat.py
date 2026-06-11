"""
企业微信消息发送模块
发送消息到企业微信应用
"""

import requests
import json


class WeChatWork:
    """企业微信应用消息发送类"""

    def __init__(self, corpid, corpsecret, agentid):
        """
        初始化企业微信配置

        Args:
            corpid: 企业ID
            corpsecret: 应用Secret
            agentid: 应用AgentId
        """
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = None
        self.token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        self.send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"

    def get_access_token(self):
        """
        获取access_token

        Returns:
            access_token字符串
        """
        try:
            params = {
                "corpid": self.corpid,
                "corpsecret": self.corpsecret
            }

            response = requests.get(self.token_url, params=params)
            data = response.json()

            if data.get("errcode") == 0:
                self.access_token = data["access_token"]
                print("获取access_token成功")
                return self.access_token
            else:
                print(f"获取access_token失败: {data}")
                return None

        except Exception as e:
            print(f"获取access_token异常: {e}")
            return None

    def send_text_message(self, content, touser="@all"):
        """
        发送文本消息

        Args:
            content: 消息内容
            touser: 接收人，"@all"表示所有人

        Returns:
            发送结果
        """
        try:
            # 确保有access_token
            if not self.access_token:
                self.get_access_token()

            if not self.access_token:
                return {"errcode": -1, "errmsg": "获取access_token失败"}

            # 构建消息体
            data = {
                "touser": touser,
                "msgtype": "text",
                "agentid": self.agentid,
                "text": {
                    "content": content
                },
                "safe": 0
            }

            # 发送请求
            params = {"access_token": self.access_token}
            response = requests.post(
                self.send_url,
                params=params,
                json=data
            )

            result = response.json()

            if result.get("errcode") == 0:
                print("消息发送成功")
            else:
                print(f"消息发送失败: {result}")

            return result

        except Exception as e:
            print(f"发送消息异常: {e}")
            return {"errcode": -1, "errmsg": str(e)}

    def send_markdown_message(self, content, touser="@all"):
        """
        发送Markdown消息（企业微信支持的markdown格式）

        Args:
            content: Markdown格式的内容
            touser: 接收人

        Returns:
            发送结果
        """
        try:
            # 确保有access_token
            if not self.access_token:
                self.get_access_token()

            if not self.access_token:
                return {"errcode": -1, "errmsg": "获取access_token失败"}

            # 构建消息体
            data = {
                "touser": touser,
                "msgtype": "markdown",
                "agentid": self.agentid,
                "markdown": {
                    "content": content
                }
            }

            # 发送请求
            params = {"access_token": self.access_token}
            response = requests.post(
                self.send_url,
                params=params,
                json=data
            )

            result = response.json()

            if result.get("errcode") == 0:
                print("Markdown消息发送成功")
            else:
                print(f"Markdown消息发送失败: {result}")

            return result

        except Exception as e:
            print(f"发送Markdown消息异常: {e}")
            return {"errcode": -1, "errmsg": str(e)}


def send_to_wechat(content, config, msg_type="text"):
    """
    发送消息到企业微信的便捷函数

    Args:
        content: 消息内容
        config: 配置字典，包含corpid, corpsecret, agentid
        msg_type: 消息类型，"text"或"markdown"

    Returns:
        发送结果
    """
    wechat = WeChatWork(
        corpid=config["wechat"]["corpid"],
        corpsecret=config["wechat"]["corpsecret"],
        agentid=config["wechat"]["agentid"]
    )

    if msg_type == "markdown":
        return wechat.send_markdown_message(content)
    else:
        return wechat.send_text_message(content)


if __name__ == "__main__":
    # 测试
    test_config = {
        "wechat": {
            "corpid": "test_corpid",
            "corpsecret": "test_corpsecret",
            "agentid": "1000002"
        }
    }

    # 注意：测试时需要替换为真实的配置
    print("企业微信模块加载成功")
    print("实际使用时请提供真实的corpid和corpsecret")
