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
            "summary": "国家发改委今日发布《新能源产业发展规划》，提出到2030年新能源装机容量目标，推动能源结构优化升级。规划明确，到2030年风电、太阳能发电总装机容量将达到12亿千瓦以上，非化石能源消费比重提高到25%左右。",
            "source": "新华网",
            "url": "https://www.xinhuanet.com",
            "keyword": "经济政策"
        },
        {
            "title": f"国家能源局召开电力市场改革工作会议（{today}）",
            "summary": "国家能源局召开专题会议，研究部署下一阶段电力市场化改革重点任务。会议指出，今年前5个月全国电力市场化交易电量达到2.3万亿千瓦时，同比增长18.5%，占全社会用电量比重提升至62%。",
            "source": "国家能源局",
            "url": "https://www.nea.gov.cn",
            "keyword": "电力行业"
        },
        {
            "title": f"国务院常务会议部署能源保供稳价工作（{today}）",
            "summary": "国务院常务会议研究部署能源保供稳价措施，确保经济社会发展用能需求。会议强调，要发挥煤炭煤电兜底保障作用，加强油气储备能力建设，今年新增煤炭产能3亿吨/年，油气储备能力提升15%。",
            "source": "中国政府网",
            "url": "https://www.gov.cn",
            "keyword": "经济政策"
        },
        {
            "title": f"全国电力市场化交易规模持续扩大（{today}）",
            "summary": "今年1-5月，全国电力市场化交易电量达到2.3万亿千瓦时，同比增长18.5%。其中，跨省跨区交易电量4500亿千瓦时，同比增长22.3%。现货市场交易电量占比提升至15%，市场价格发现功能逐步显现。",
            "source": "中国电力新闻网",
            "url": "http://www.cpnn.com.cn",
            "keyword": "电力行业"
        },
        {
            "title": f"新能源消纳水平再创新高（{today}）",
            "summary": "国家电网数据显示，今年新能源利用率达到97.8%，同比提高0.5个百分点。风电、光伏发电量合计达到8500亿千瓦时，占总发电量的18.2%，同比提高2.1个百分点。弃风弃光率下降至2.2%，创历史新低。",
            "source": "国家电网",
            "url": "https://www.sgcc.com.cn",
            "keyword": "新能源"
        },
        {
            "title": f"工信部：加快推进AI在制造业深度应用（{today}）",
            "summary": "工信部印发《人工智能赋能新型工业化实施方案》，提出到2027年，AI在制造业重点领域应用深度和广度显著提升。方案明确，将在电子信息、装备制造、汽车、钢铁、石化化工等重点行业打造100个以上AI应用标杆案例，带动行业效率提升30%以上。",
            "source": "工信部官网",
            "url": "https://www.miit.gov.cn",
            "keyword": "AI应用"
        },
        {
            "title": f"全球AI芯片市场规模突破千亿美元（{today}）",
            "summary": "据市场研究机构最新报告，2026年全球AI芯片市场规模预计达到1050亿美元，同比增长35%。其中，训练芯片市场约450亿美元，推理芯片市场约600亿美元。中国企业在全球AI芯片市场份额提升至15%，华为昇腾、寒武纪等国产品牌加速崛起。",
            "source": "科技日报",
            "url": "https://www.stdaily.com",
            "keyword": "AI技术"
        },
        {
            "title": f"大模型技术持续突破，国产大模型性能接近国际先进水平（{today}）",
            "summary": "最新评测显示，国产大模型在中文理解、代码生成、数学推理等核心能力上取得显著进步。小米MiMo、通义千问、文心一言等模型在多项基准测试中表现优异，部分指标已接近GPT-4水平。截至目前，国内备案的大模型数量已超过300个，应用场景覆盖办公、教育、医疗、金融等20多个领域。",
            "source": "中国科学报",
            "url": "https://www.sciencenet.cn",
            "keyword": "AI技术"
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
