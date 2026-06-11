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
        prompt = f"""你是一个资深的财经和科技新闻分析师。请根据以下新闻，生成一份详细、专业的每日简报。

要求：
1. 使用中文，语言专业但易读
2. **新闻要详细展开**：不要精简，保留关键数据、数字、百分比、时间点
3. **数据驱动**：引用新闻中的具体数据，如增长百分比、规模数据、时间目标等
4. **深度分析**：每条新闻后添加"影响分析"，说明对行业/市场的影响
5. **关联性分析**：分析经济政策、电力行业、AI技术之间的关联和相互影响
6. **趋势总结**：在最后添加一个"趋势与展望"板块，总结：
   - 今日新闻反映的整体趋势
   - 对未来1-3个月的预判
   - 值得关注的投资方向或机会
   - 潜在的风险点
7. 适当添加emoji让内容更易读
8. 结构清晰，使用标题和要点列表

今日新闻：
{news_content}

请生成详细版每日简报："""

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
            max_tokens=3000,
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
    summary = "📰 每日财经与科技简报\n\n"
    summary += "## 今日要闻\n\n"

    for i, news in enumerate(news_list, 1):
        if "AI" in news.get("keyword", "") or "人工智能" in news.get("keyword", ""):
            emoji = "🤖"
        elif "政策" in news.get("keyword", ""):
            emoji = "🏛️"
        else:
            emoji = "⚡"

        summary += f"### {emoji} {i}. {news['title']}\n\n"
        summary += f"**来源：** {news.get('source', '未知')}\n\n"
        summary += f"{news['summary']}\n\n"
        summary += f"**影响分析：** 该消息对相关行业将产生重要影响，建议持续关注后续政策落地和市场反应。\n\n"

    summary += "---\n\n"
    summary += "## 📊 趋势与展望\n\n"
    summary += "**整体趋势：**\n"
    summary += "- 经济政策持续推进能源结构转型\n"
    summary += "- 电力市场化改革进入深水区\n"
    summary += "- AI技术加速赋能传统行业\n\n"
    summary += "**关注要点：**\n"
    summary += "- 新能源产业链投资机会\n"
    summary += "- 电力交易市场化带来的机遇\n"
    summary += "- AI+能源领域的创新应用\n\n"
    summary += "**风险提示：**\n"
    summary += "- 关注国际能源价格波动\n"
    summary += "- 留意政策执行力度变化\n"

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
