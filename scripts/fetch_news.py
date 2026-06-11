"""
获取新闻模块
从公开新闻源获取经济政策和电力行业新闻
"""

import requests
import json
from datetime import datetime, timedelta


def fetch_news_from_newsapi(keywords, max_articles=5):
    """
    从NewsAPI获取新闻（免费额度）
    需要注册 https://newsapi.org 获取API Key
    """
    # 如果没有NewsAPI Key，返回示例数据
    # 实际使用时替换为真实API调用
    return get_sample_news(keywords, max_articles)


def fetch_news_from_rss(keywords, max_articles=5):
    """
    从RSS源获取新闻
    可以添加多个RSS源
    """
    # RSS源列表（可以根据需要添加）
    rss_feeds = {
        "经济政策": [
            "http://www.gov.cn/rss/govall.xml",
        ],
        "电力行业": [
            "https://news.bjx.com.cn/rss.xml",
        ]
    }

    # 简化版本：返回示例数据
    # 实际实现需要解析RSS XML
    return get_sample_news(keywords, max_articles)


def get_sample_news(keywords, max_articles=5):
    """
    示例新闻数据
    实际使用时替换为真实API调用
    """
    today = datetime.now().strftime("%Y年%m月%d日")

    sample_news = [
        {
            "title": f"国家发改委发布新能源产业发展规划（{today}）",
            "summary": "国家发改委今日发布《新能源产业发展规划》，提出到2030年新能源装机容量目标，推动能源结构优化升级。",
            "source": "新华网",
            "url": "https://www.xinhuanet.com",
            "keyword": "经济政策"
        },
        {
            "title": f"国家能源局召开电力市场改革工作会议（{today}）",
            "summary": "国家能源局召开专题会议，研究部署下一阶段电力市场化改革重点任务，推动建设全国统一电力市场体系。",
            "source": "国家能源局",
            "url": "https://www.nea.gov.cn",
            "keyword": "电力行业"
        },
        {
            "title": f"国务院常务会议部署能源保供稳价工作（{today}）",
            "summary": "国务院常务会议研究部署能源保供稳价措施，确保经济社会发展用能需求，维护能源安全。",
            "source": "中国政府网",
            "url": "https://www.gov.cn",
            "keyword": "经济政策"
        },
        {
            "title": f"全国电力市场化交易规模持续扩大（{today}）",
            "summary": "今年1-5月，全国电力市场化交易电量同比增长15.2%，市场在电力资源配置中的作用进一步增强。",
            "source": "中国电力新闻网",
            "url": "http://www.cpnn.com.cn",
            "keyword": "电力行业"
        },
        {
            "title": f"新能源消纳水平再创新高（{today}）",
            "summary": "国家电网数据显示，今年新能源利用率达到97.5%，风电、光伏发电量占比持续提升。",
            "source": "国家电网",
            "url": "https://www.sgcc.com.cn",
            "keyword": "新能源"
        }
    ]

    # 根据关键词过滤
    filtered_news = []
    for news in sample_news:
        if any(kw in news["title"] or kw in news["summary"] for kw in keywords):
            filtered_news.append(news)

    # 如果过滤后不足，返回所有新闻
    if len(filtered_news) < max_articles:
        filtered_news = sample_news

    return filtered_news[:max_articles]


def main(keywords, max_articles=5):
    """
    主函数：获取新闻
    """
    print(f"正在获取新闻，关键词：{keywords}")

    # 尝试从多个源获取新闻
    all_news = []

    # 方式1：示例数据（开发测试用）
    news = get_sample_news(keywords, max_articles)
    all_news.extend(news)

    # 方式2：NewsAPI（需要API Key）
    # news = fetch_news_from_newsapi(keywords, max_articles)
    # all_news.extend(news)

    # 去重（按标题）
    seen_titles = set()
    unique_news = []
    for article in all_news:
        if article["title"] not in seen_titles:
            seen_titles.add(article["title"])
            unique_news.append(article)

    print(f"获取到 {len(unique_news)} 条新闻")
    return unique_news[:max_articles]


if __name__ == "__main__":
    # 测试
    keywords = ["经济政策", "电力行业", "新能源"]
    news = main(keywords)
    for i, article in enumerate(news, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   {article['summary']}")
