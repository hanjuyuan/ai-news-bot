#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周汇总模块
收集一周内的AI新闻并生成周总结
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.daily_news import DailyNewsScraper

class WeeklySummaryGenerator:
    def __init__(self):
        self.data_dir = 'data'
        self.daily_files = []

    def collect_weekly_news(self) -> List[Dict[str, Any]]:
        """收集过去一周的新闻"""
        news_collection = []

        # 计算过去7天的日期
        today = datetime.now()
        week_dates = []

        for i in range(7):
            date = today - timedelta(days=i)
            week_dates.append(date.strftime('%Y-%m-%d'))

        # 收集每天的文件
        for date_str in week_dates:
            daily_file = f'{self.data_dir}/daily_news.json'
            if os.path.exists(daily_file):
                try:
                    with open(daily_file, 'r', encoding='utf-8') as f:
                        daily_data = json.load(f)
                        if daily_data.get('date') == date_str:
                            news_collection.extend(daily_data.get('news', []))
                        else:
                            # 如果是其他日期的文件，加载最近的7天数据
                            news_collection.extend(daily_data.get('news', []))
                except Exception as e:
                    print(f"读取{date_str}的文件时出错: {e}")

        # 去重和排序
        seen_links = set()
        unique_news = []

        for news in news_collection:
            if news.get('link') not in seen_links:
                seen_links.add(news.get('link'))
                unique_news.append(news)

        return unique_news

    def categorize_weekly_news(self, news_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """按类别整理一周新闻"""
        categories = {
            'product': [],
            'research': [],
            'policy': [],
            'funding': [],
            'competition': []
        }

        for news in news_list:
            category = news.get('category', 'product')
            if category in categories:
                categories[category].append(news)

        return categories

    def generate_weekly_summary(self) -> str:
        """生成周总结"""
        try:
            # 收集本周新闻
            weekly_news = self.collect_weekly_news()

            if not weekly_news:
                # 如果没有现有数据，尝试重新抓取
                scraper = DailyNewsScraper()
                recent_news = scraper.scrape_news()
                weekly_news = recent_news

            if not weekly_news:
                return "🗓️ **本周AI大盘点**\n\n本周似乎没什么大新闻，AI行业也在休假？😄"

            # 分类整理
            categories = self.categorize_weekly_news(weekly_news)

            start_date = (datetime.now() - timedelta(days=6)).strftime('%m月%d日')
            end_date = datetime.now().strftime('%m月%d日')

            summary = f"🗓️ **本周AI大盘点** ({start_date} - {end_date})\n\n"

            total_count = len(weekly_news)
            summary += f"本周共监测到 {total_count} 条AI相关新闻，以下是精选内容：\n\n"

            # 按类别展示
            emoji_map = {'product': '📱', 'research': '🔬', 'policy': '📋', 'funding': '💰', 'competition': '🏆'}
            category_names = {
                'product': '📱 产品发布',
                'research': '🔬 技术突破',
                'policy': '📋 政策动态',
                'funding': '💰 融资消息',
                'competition': '🏆 行业竞争'
            }

            for category in ['product', 'research', 'funding', 'policy', 'competition']:
                news_in_category = categories.get(category, [])
                if news_in_category:
                    summary += f"**{category_names[category]}** ({len(news_in_category)}条)\n"

                    # 每个分类取最重要的1-2条
                    important_news = news_in_category[:2]
                    for news in important_news:
                        title = self._format_title(news['title'])
                        summary += f"• {title}\n"
                        summary += f"  [详情]({news['link']})\n"
                    summary += "\n"

            # 本周热点趋势
            summary += self._generate_trend_analysis(weekly_news)

            summary += datetime.now().strftime("\n📅 更新时间：%Y-%m-%d")

            return summary

        except Exception as e:
            error_msg = f"生成周总结时出错了: {str(e)}"
            print(error_msg)
            return error_msg

    def _format_title(self, title: str) -> str:
        """格式化标题"""
        import html
        title = html.unescape(title)
        max_length = 40
        if len(title) > max_length:
            return title[:max_length] + "..."
        return title

    def _generate_trend_analysis(self, news_list: List[Dict[str, Any]]) -> str:
        """生成热点趋势分析"""
        trend_topics = []

        # 简单提取高频关键词
        keywords_count = {}
        common_keywords = ['ChatGPT', 'GPT', '大模型', 'AI', '人工智能', '机器学习',
                          '深度学习', '生成式', '开源', 'robo', 'Agent']

        for news in news_list:
            title = news.get('title', '').lower()
            for keyword in common_keywords:
                if keyword.lower() in title:
                    keywords_count[keyword] = keywords_count.get(keyword, 0) + 1

        # 找出热点话题
        if keywords_count:
            top_keywords = sorted(keywords_count.items(), key=lambda x: x[1], reverse=True)[:3]
            for keyword, count in top_keywords:
                if count >= 2:
                    trend_topics.append(keyword)

        if trend_topics:
            return f"\n📈 **本周热点**：{'、'.join(trend_topics)} 讨论度最高！\n\n"
        else:
            return "\n📈 **本周观察**：AI领域动态比较分散，关注度比较平均。\n\n"

    def save_weekly_data(self, summary: str):
        """保存周总结数据"""
        try:
            week_start = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
            week_end = datetime.now().strftime('%Y-%m-%d')

            weekly_data = {
                'week_range': f"{week_start}_to_{week_end}",
                'summary': summary,
                'total_news': len(self.collect_weekly_news()),
                'timestamp': datetime.now().isoformat()
            }

            os.makedirs(self.data_dir, exist_ok=True)
            with open(f'{self.data_dir}/weekly_summary.json', 'w', encoding='utf-8') as f:
                json.dump(weekly_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"保存周总结失败: {e}")

if __name__ == "__main__":
    generator = WeeklySummaryGenerator()
    summary = generator.generate_weekly_summary()
    generator.save_weekly_data(summary)
    print(summary)