"""
每日新闻推送主程序
整合新闻获取、AI摘要生成、Server酱推送
"""

import json
import os
import sys
from datetime import datetime

# 添加scripts目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_news import main as fetch_news
from generate_summary import main as generate_summary
from send_serverchan import send_to_serverchan


def load_config():
    """
    加载配置文件

    优先级：
    1. 环境变量（GitHub Secrets）
    2. config.json文件
    """
    config = {
        "serverchan": {
            "sendkey": os.getenv("SERVERCHAN_SENDKEY", "")
        },
        "ai": {
            "api_key": os.getenv("AI_API_KEY", ""),
            "api_endpoint": os.getenv("AI_API_ENDPOINT", "https://api.xiaomimimo.com/v1/chat/completions"),
            "model": os.getenv("AI_MODEL", "MiMo")
        },
        "news": {
            "keywords": ["经济政策", "电力行业", "新能源", "电力市场", "能源改革"],
            "max_articles": 5
        }
    }

    # 如果环境变量为空，尝试从config.json读取
    if not config["serverchan"]["sendkey"]:
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                # 合并配置
                for key in config:
                    if key in file_config:
                        config[key].update(file_config[key])
        except Exception as e:
            print(f"读取config.json失败: {e}")

    return config


def validate_config(config):
    """
    验证配置是否完整

    Args:
        config: 配置字典

    Returns:
        (bool, str) - (是否有效, 错误信息)
    """
    # 检查Server酱配置
    if not config["serverchan"]["sendkey"]:
        return False, "缺少Server酱SendKey"

    # 检查AI配置
    if not config["ai"]["api_key"]:
        return False, "缺少AI API Key"

    return True, ""


def format_message(news_list, ai_summary):
    """
    格式化最终推送的消息（Markdown格式）

    Args:
        news_list: 新闻列表
        ai_summary: AI生成的摘要

    Returns:
        格式化后的Markdown文本
    """
    today = datetime.now().strftime("%Y年%m月%d日")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]

    message = f"# 🌅 早安！今日财经简报\n\n"
    message += f"📅 **{today} {weekday}**\n\n"
    message += "---\n\n"

    # 添加AI摘要
    message += ai_summary + "\n\n"

    message += "---\n\n"
    message += "## 📌 新闻来源\n\n"

    # 添加新闻来源
    for i, news in enumerate(news_list, 1):
        source = news.get("source", "未知")
        title = news["title"][:20] + "..." if len(news["title"]) > 20 else news["title"]
        message += f"{i}. {title} - *{source}*\n"

    message += "\n---\n\n"
    message += "💡 *祝您今日工作顺利！*"

    return message


def main():
    """
    主函数
    """
    print("=" * 50)
    print("每日新闻推送系统启动")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 1. 加载配置
    print("\n[1/4] 加载配置...")
    config = load_config()

    # 2. 验证配置
    print("[2/4] 验证配置...")
    is_valid, error_msg = validate_config(config)
    if not is_valid:
        print(f"❌ 配置验证失败: {error_msg}")
        sys.exit(1)
    print("✅ 配置验证通过")

    # 3. 获取新闻
    print("\n[3/4] 获取新闻...")
    try:
        news_list = fetch_news(
            keywords=config["news"]["keywords"],
            max_articles=config["news"]["max_articles"]
        )
        if not news_list:
            print("❌ 未获取到新闻")
            sys.exit(1)
        print(f"✅ 获取到 {len(news_list)} 条新闻")
    except Exception as e:
        print(f"❌ 获取新闻失败: {e}")
        sys.exit(1)

    # 4. 生成AI摘要
    print("\n[4/4] 生成AI摘要...")
    try:
        ai_summary = generate_summary(news_list, config)
        print("✅ AI摘要生成完成")
    except Exception as e:
        print(f"⚠️ AI摘要生成失败，使用默认摘要: {e}")
        from generate_summary import generate_default_summary
        ai_summary = generate_default_summary(news_list)

    # 5. 格式化消息
    print("\n正在格式化消息...")
    title = f"📰 每日财经简报 {datetime.now().strftime('%m/%d')}"
    content = format_message(news_list, ai_summary)

    # 6. 通过Server酱发送到微信
    print("\n正在通过Server酱发送到微信...")
    result = send_to_serverchan(title, content, config["serverchan"]["sendkey"])

    if result.get("code") == 0:
        print("\n" + "=" * 50)
        print("✅ 消息推送成功！")
        print("=" * 50)
        print("\n消息预览：")
        print("-" * 30)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("-" * 30)
    else:
        print(f"\n❌ 消息推送失败: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
