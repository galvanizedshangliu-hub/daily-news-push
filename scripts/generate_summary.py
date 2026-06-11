"""
AI摘要生成模块
使用小米MiMo API生成个性化新闻摘要
"""

import json
import requests
from openai import OpenAI


def generate_summary(news_list, api_key, api_endpoint, model="MiMo"):
    """
    调用AI API生成个性化新闻摘要

    Args:
        news_list: 新闻列表
        api_key: API密钥
        api_endpoint: API端点
        model: 模型名称

    Returns:
        格式化的摘要文本
    """
    try:
        # 构建新闻内容
        news_content = ""
        for i, news in enumerate(news_list, 1):
            news_content += f"\n{i}. 【{news.get('keyword', '综合')}】{news['title']}\n"
            news_content += f"   来源：{news.get('source', '未知')}\n"
            news_content += f"   摘要：{news['summary']}\n"

        # 构建提示词
        prompt = f"""你是一个专业的财经新闻分析师。请根据以下新闻，生成一份简洁、专业的每日简报。

要求：
1. 使用中文
2. 语言简洁明了，突出重点
3. 对经济政策和电力行业进行关联性分析
4. 提供简短的市场影响分析
5. 适当添加emoji让内容更易读
6. 结构清晰，使用要点列表

今日新闻：
{news_content}

请生成每日简报："""

        # 调用小米MiMo API（使用OpenAI兼容格式）
        client = OpenAI(
            api_key=api_key,
            base_url=api_endpoint.replace("/chat/completions", "")
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的财经新闻分析师，擅长分析经济政策和电力行业动态。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )

        # 提取生成的摘要
        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        print(f"AI摘要生成失败: {e}")
        # 返回默认摘要
        return generate_default_summary(news_list)


def generate_default_summary(news_list):
    """
    生成默认摘要（当AI API调用失败时使用）
    """
    summary = "📰 每日财经简报\n\n"
    summary += "今日要闻：\n\n"

    for i, news in enumerate(news_list, 1):
        emoji = "🏛️" if "政策" in news.get("keyword", "") else "⚡"
        summary += f"{emoji} {i}. {news['title']}\n"
        summary += f"   {news['summary']}\n\n"

    summary += "💡 关注要点：\n"
    summary += "- 经济政策动向对市场的影响\n"
    summary += "- 电力行业改革进展\n"
    summary += "- 新能源发展趋势\n"

    return summary


def main(news_list, config):
    """
    主函数：生成AI摘要
    """
    print("正在生成AI摘要...")

    api_key = config["ai"]["api_key"]
    api_endpoint = config["ai"]["api_endpoint"]
    model = config["ai"].get("model", "MiMo")

    summary = generate_summary(news_list, api_key, api_endpoint, model)

    print("AI摘要生成完成")
    return summary


if __name__ == "__main__":
    # 测试
    test_news = [
        {
            "title": "国家发改委发布新能源政策",
            "summary": "推动能源结构优化升级",
            "keyword": "经济政策"
        },
        {
            "title": "电力市场化改革加速",
            "summary": "全国统一电力市场建设提速",
            "keyword": "电力行业"
        }
    ]

    config = {
        "ai": {
            "api_key": "your-api-key",
            "api_endpoint": "https://api.xiaomimimo.com/v1/chat/completions",
            "model": "MiMo"
        }
    }

    print(generate_default_summary(test_news))
