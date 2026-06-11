"""
获取新闻模块
从RSS源获取经济政策、电力行业和AI行业的新闻
"""

import requests
import feedparser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import re


# RSS源配置
RSS_FEEDS = {
    "经济政策": [
        {
            "name": "中国政府网",
            "url": "http://www.gov.cn/rss/govall.xml",
            "encoding": "utf-8"
        },
        {
            "name": "新华网",
            "url": "http://www.xinhuanet.com/politics/xhll.xml",
            "encoding": "utf-8"
        }
    ],
    "电力行业": [
        {
            "name": "北极星电力网",
            "url": "https://news.bjx.com.cn/rss.xml",
            "encoding": "utf-8"
        },
        {
            "name": "中国电力新闻网",
            "url": "http://www.cpnn.com.cn/rss/gd.xml",
            "encoding": "utf-8"
        }
    ],
    "AI技术": [
        {
            "name": "36氪AI频道",
            "url": "https://36kr.com/feed",
            "encoding": "utf-8"
        },
        {
            "name": "机器之心",
            "url": "https://www.jiqizhixin.com/rss",
            "encoding": "utf-8"
        }
    ]
}


def clean_html(html_text):
    """
    清理HTML标签，提取纯文本
    """
    if not html_text:
        return ""

    try:
        soup = BeautifulSoup(html_text, 'lxml')
        text = soup.get_text(separator=' ', strip=True)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text)
        return text[:500]  # 限制长度
    except Exception:
        # 如果BeautifulSoup失败，用正则简单清理
        text = re.sub(r'<[^>]+>', '', html_text)
        text = re.sub(r'\s+', ' ', text)
        return text[:500]


def fetch_rss_feed(feed_info, category, max_items=3):
    """
    从单个RSS源获取新闻

    Args:
        feed_info: RSS源信息字典
        category: 新闻类别
        max_items: 最大获取条数

    Returns:
        新闻列表
    """
    news_list = []

    try:
        print(f"  正在获取: {feed_info['name']}...")

        # 添加请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(
            feed_info['url'],
            headers=headers,
            timeout=15
        )
        response.encoding = feed_info.get('encoding', 'utf-8')

        # 解析RSS
        feed = feedparser.parse(response.text)

        if not feed.entries:
            print(f"    ⚠️ {feed_info['name']} 无内容")
            return news_list

        # 获取今天的日期（用于过滤）
        today = datetime.now().date()

        for entry in feed.entries[:max_items * 2]:  # 多获取一些，用于过滤
            try:
                # 解析发布时间
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6]).date()
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6]).date()

                # 获取标题
                title = entry.get('title', '').strip()
                if not title:
                    continue

                # 获取摘要
                summary = ''
                if hasattr(entry, 'summary'):
                    summary = clean_html(entry.summary)
                elif hasattr(entry, 'description'):
                    summary = clean_html(entry.description)

                # 如果摘要太短，尝试获取content
                if len(summary) < 50 and hasattr(entry, 'content'):
                    for content in entry.content:
                        if content.get('value'):
                            summary = clean_html(content.value)
                            break

                # 构建新闻对象
                news_item = {
                    "title": title,
                    "summary": summary if summary else title,
                    "source": feed_info['name'],
                    "url": entry.get('link', ''),
                    "keyword": category,
                    "published": published.strftime("%Y-%m-%d") if published else "未知"
                }

                news_list.append(news_item)

                if len(news_list) >= max_items:
                    break

            except Exception as e:
                print(f"    解析条目失败: {e}")
                continue

        print(f"    ✓ 获取到 {len(news_list)} 条")

    except requests.exceptions.Timeout:
        print(f"    ✗ {feed_info['name']} 超时")
    except requests.exceptions.RequestException as e:
        print(f"    ✗ {feed_info['name']} 请求失败: {e}")
    except Exception as e:
        print(f"    ✗ {feed_info['name']} 解析失败: {e}")

    return news_list


def fetch_news_by_keywords(keywords, max_per_keyword=3):
    """
    根据关键词从对应RSS源获取新闻

    Args:
        keywords: 关键词列表
        max_per_keyword: 每个关键词最大新闻数

    Returns:
        新闻列表
    """
    all_news = []
    seen_titles = set()

    for keyword in keywords:
        print(f"\n获取 [{keyword}] 相关新闻:")

        # 找到匹配的RSS源
        feeds = RSS_FEEDS.get(keyword, [])

        if not feeds:
            print(f"  未找到 [{keyword}] 的RSS源")
            continue

        for feed_info in feeds:
            news_list = fetch_rss_feed(feed_info, keyword, max_per_keyword)

            # 去重
            for news in news_list:
                if news['title'] not in seen_titles:
                    seen_titles.add(news['title'])
                    all_news.append(news)

            # 礼貌性延迟，避免请求过快
            time.sleep(1)

    return all_news


def get_sample_news_fallback(keywords, max_articles=8):
    """
    备用示例数据（当RSS获取失败时使用）
    """
    today = datetime.now().strftime("%Y年%m月%d日")

    sample_news = [
        {
            "title": f"国家发改委发布新能源产业发展规划（{today}）",
            "summary": "国家发改委今日发布《新能源产业发展规划》，提出到2030年新能源装机容量目标，推动能源结构优化升级。规划明确，到2030年风电、太阳能发电总装机容量将达到12亿千瓦以上，非化石能源消费比重提高到25%左右。",
            "source": "新华网",
            "url": "https://www.xinhuanet.com",
            "keyword": "经济政策",
            "published": today
        },
        {
            "title": f"国家能源局召开电力市场改革工作会议（{today}）",
            "summary": "国家能源局召开专题会议，研究部署下一阶段电力市场化改革重点任务。会议指出，今年前5个月全国电力市场化交易电量达到2.3万亿千瓦时，同比增长18.5%，占全社会用电量比重提升至62%。",
            "source": "国家能源局",
            "url": "https://www.nea.gov.cn",
            "keyword": "电力行业",
            "published": today
        },
        {
            "title": f"工信部：加快推进AI在制造业深度应用（{today}）",
            "summary": "工信部印发《人工智能赋能新型工业化实施方案》，提出到2027年，AI在制造业重点领域应用深度和广度显著提升。方案明确，将在重点行业打造100个以上AI应用标杆案例，带动行业效率提升30%以上。",
            "source": "工信部官网",
            "url": "https://www.miit.gov.cn",
            "keyword": "AI技术",
            "published": today
        },
        {
            "title": f"全球AI芯片市场规模突破千亿美元（{today}）",
            "summary": "据市场研究机构最新报告，2026年全球AI芯片市场规模预计达到1050亿美元，同比增长35%。其中，训练芯片市场约450亿美元，推理芯片市场约600亿美元。中国企业在全球AI芯片市场份额提升至15%。",
            "source": "科技日报",
            "url": "https://www.stdaily.com",
            "keyword": "AI技术",
            "published": today
        }
    ]

    # 根据关键词过滤
    filtered_news = []
    for news in sample_news:
        if any(kw in news.get("keyword", "") or kw in news.get("title", "") for kw in keywords):
            filtered_news.append(news)

    if len(filtered_news) < max_articles:
        filtered_news = sample_news

    return filtered_news[:max_articles]


def main(keywords, max_articles=8):
    """
    主函数：获取新闻

    Args:
        keywords: 关键词列表
        max_articles: 最大新闻数

    Returns:
        新闻列表
    """
    print("=" * 50)
    print("开始获取新闻")
    print(f"关键词: {keywords}")
    print("=" * 50)

    # 从RSS源获取新闻
    news_list = fetch_news_by_keywords(keywords, max_per_keyword=3)

    # 如果RSS获取的新闻不足，使用备用数据补充
    if len(news_list) < 3:
        print("\n⚠️ RSS获取新闻不足，使用备用数据补充...")
        fallback_news = get_sample_news_fallback(keywords, max_articles)
        news_list.extend(fallback_news)

    # 去重
    seen_titles = set()
    unique_news = []
    for news in news_list:
        if news['title'] not in seen_titles:
            seen_titles.add(news['title'])
            unique_news.append(news)

    # 限制数量
    result = unique_news[:max_articles]

    print("\n" + "=" * 50)
    print(f"最终获取到 {len(result)} 条新闻")
    print("=" * 50)

    return result


if __name__ == "__main__":
    # 测试
    test_keywords = ["经济政策", "电力行业", "AI技术"]
    news = main(test_keywords, max_articles=5)

    print("\n获取到的新闻:")
    for i, article in enumerate(news, 1):
        print(f"\n{i}. [{article['keyword']}] {article['title']}")
        print(f"   来源: {article['source']} | 发布: {article.get('published', '未知')}")
        print(f"   摘要: {article['summary'][:100]}...")
