#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日AI新闻抓取模块
从多个数据源聚合最新的AI相关新闻
"""

import requests
import json
import hashlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser
import os
import sys
from typing import List, Dict, Any

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import NEWS_SOURCES, MESSAGE_SETTINGS, DATA_DIR

class DailyNewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.news_items = []

    def scrape_news(self) -> List[Dict[str, Any]]:
        """主函数：从所有数据源抓取新闻"""
        all_news = []

        # 抓取RSS源的新闻
        for source_name, source_config in NEWS_SOURCES.items():
            try:
                if source_config['type'] == 'rss':
                    news = self._scrape_rss(source_config['url'], source_name)
                else:
                    news = self._scrape_web(source_config['url'], source_name)

                all_news.extend(news)
                print(f"成功从 {source_name} 抓取 {len(news)} 条新闻")

            except Exception as e:
                print(f"从 {source_name} 抓取新闻失败: {e}")

        # 去重
        unique_news = self._deduplicate_news(all_news)

        # 按时间排序，取最新的几条
        sorted_news = sorted(unique_news, key=lambda x: x.get('published', ''), reverse=True)
        return sorted_news[:MESSAGE_SETTINGS['max_daily_items']]

    def _scrape_rss(self, url: str, source: str) -> List[Dict[str, Any]]:
        """抓取RSS源"""
        try:
            feed = feedparser.parse(url)
            news = []

            for entry in feed.entries[:10]:  # 只取最近10条
                news_item = {
                    'title': entry.title,
                    'link': entry.link,
                    'summary': self._clean_text(entry.get('summary', '')[:200]),
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source': source,
                    'category': self._classify_news(entry.title)
                }
                news.append(news_item)

            return news
        except Exception as e:
            print(f"RSS抓取失败 {url}: {e}")
            return []

    def _scrape_web(self, url: str, source: str) -> List[Dict[str, Any]]:
        """从网页抓取新闻（备用方案）"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            news = []

            # 根据不同的网站结构进行解析
            if '36kr' in url:
                news = self._scrape_36kr(soup)
            elif 'qbitai' in url:
                news = self._scrape_qbitai(soup)
            else:
                return []

            for item in news:
                item['source'] = source
                item['category'] = self._classify_news(item['title'])

            return news
        except Exception as e:
            print(f"网页抓取失败 {url}: {e}")
            return []

    def _scrape_36kr(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """抓取36氪AI频道"""
        news = []
        articles = soup.find_all('div', class_='article-item')

        for article in articles[:5]:
            try:
                title_elem = article.find('a', class_='article-item-title')
                if title_elem:
                    title = title_elem.text.strip()
                    link = 'https://36kr.com' + title_elem.get('href', '')
                    summary = article.find('div', class_='article-item-description')
                    summary = summary.text.strip()[:150] if summary else ''

                    news.append({
                        'title': title,
                        'link': link,
                        'summary': self._clean_text(summary),
                        'published': datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"解析36氪文章出错: {e}")
                continue

        return news

    def _scrape_qbitai(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """抓取量子位"""
        news = []
        articles = soup.find_all('article')[:5]

        for article in articles:
            try:
                title_elem = article.find('h2')
                if title_elem:
                    title = title_elem.text.strip()
                    link = article.find('a').get('href', '')
                    summary_elem = article.find('div', class_='entry-summary')
                    summary = summary_elem.text.strip()[:150] if summary_elem else ''

                    news.append({
                        'title': title,
                        'link': link,
                        'summary': self._clean_text(summary),
                        'published': datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"解析量子位文章出错: {e}")
                continue

        return news

    def _clean_text(self, text: str) -> str:
        """清理和简化文本"""
        if not text:
            return ""

        # 移除HTML标签
        import re
        text = re.sub(r'<[^>]+>', '', text)

        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)

        # 确保是简体中文
        text = text.strip()

        return text

    def _classify_news(self, title: str) -> str:
        """简单分类新闻类型"""
        title_lower = title.lower()

        if any(kw in title_lower for kw in ['产品', '发布', '推出', '上线']):
            return 'product'
        elif any(kw in title_lower for kw in ['研究', '论文', '技术', '模型']):
            return 'research'
        elif any(kw in title_lower for kw in ['政策', '法规', '监管']):
            return 'policy'
        elif any(kw in title_lower for kw in ['融资', '投资', '收购']):
            return 'funding'
        elif any(kw in title_lower for kw in ['比赛', '竞赛', '挑战']):
            return 'competition'
        else:
            return 'product'  # 默认分类

    def _deduplicate_news(self, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """使用标题相似度去重"""
        seen_hashes = set()
        unique_news = []

        for news in news_list:
            title_hash = hashlib.md5(news['title'].encode()).hexdigest()

            if title_hash not in seen_hashes:
                seen_hashes.add(title_hash)
                unique_news.append(news)

        return unique_news

    def save_daily_news(self, news: List[Dict[str, Any]]):
        """保存每日新闻到文件"""
        os.makedirs(DATA_DIR, exist_ok=True)

        news_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'news': news,
            'timestamp': datetime.now().isoformat()
        }

        with open('data/daily_news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)

    def get_daily_news_summary(self) -> str:
        """获取格式化的每日新闻摘要"""
        try:
            daily_news = self.scrape_news()
            self.save_daily_news(daily_news)

            if not daily_news:
                return "今天没找到什么新鲜AI新闻，大家都放假了吧😅"

            emoji_map = MESSAGE_SETTINGS['emoji_map']

            summary = "📰 **今日AI新鲜事**\n\n"

            for i, news in enumerate(daily_news, 1):
                emoji = emoji_map.get(news.get('category', 'product'), '📌')
                title = self._format_title_for_dingtalk(news['title'])
                summary_text = news.get('summary', '')

                if len(summary_text) > 100:
                    summary_text = summary_text[:100] + "..."

                summary += f"{i}. {emoji} **{title}**\n"
                if summary_text:
                    summary += f"   {summary_text}\n"
                summary += f"   [查看详情]({news['link']})\n\n"

            summary += datetime.now().strftime("🕒 更新时间：%Y-%m-%d %H:%M")

            return summary

        except Exception as e:
            error_msg = f"抓取今日AI新闻时出错了: {str(e)}"
            print(error_msg)
            return error_msg

    def _format_title_for_dingtalk(self, title: str) -> str:
        """格式化标题为钉钉友好的中文"""
        # 移除HTML实体
        import html
        title = html.unescape(title)

        # 如果标题太长，截断
        max_length = 35
        if len(title) > max_length:
            return title[:max_length] + "..."

        return title

if __name__ == "__main__":
    scraper = DailyNewsScraper()
    summary = scraper.get_daily_news_summary()
    print(summary)