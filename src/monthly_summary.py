#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月汇总模块
收集整月的AI新闻并生成月度总结
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MonthlySummaryGenerator:
    def __init__(self):
        self.data_dir = 'data'

    def collect_monthly_news(self) -> List[Dict[str, Any]]:
        """收集本月所有新闻"""
        news_collection = []

        # 收集本月数据文件
        monthly_files = ['daily_news.json', 'weekly_summary.json']

        # 从每日文件中收集数据
        daily_file_path = f'{self.data_dir}/daily_news.json'
        if os.path.exists(daily_file_path):
            try:
                with open(daily_file_path, 'r', encoding='utf-8') as f:
                    daily_data = json.load(f)
                    if isinstance(daily_data, list):
                        news_collection.extend(daily_data)
                    elif isinstance(daily_data, dict) and 'news' in daily_data:
                        news_collection.extend(daily_data['news'])
            except Exception as e:
                print(f"读取每日新闻文件错误: {e}")

        # 尝试从每周总结中收集
        weekly_file_path = f'{self.data_dir}/weekly_summary.json'
        if os.path.exists(weekly_file_path):
            try:
                with open(weekly_file_path, 'r', encoding='utf-8') as f:
                    weekly_data = json.load(f)
                    # 可以尝试从总结中反推数据
            except Exception as e:
                print(f"读取每周总结文件错误: {e}")

        # 去重
        seen_links = set()
        unique_news = []
        for news in news_collection:
            if news.get('link') not in seen_links:
                seen_links.add(news.get('link'))
                unique_news.append(news)

        return unique_news

    def generate_monthly_summary(self) -> str:
        """生成本月AI行业总结"""
        try:
            monthly_news = self.collect_monthly_news()

            if not monthly_news:
                # 如果没有历史数据，生成一个友好的提示
                return self._generate_default_monthly_report()

            current_month = datetime.now().strftime('%Y年%m月')
            summary = f"📊 **{current_month} AI大盘点**\n\n"

            # 基本统计
            total_news = len(monthly_news)
            summary += f"本月共收集 {total_news} 条AI相关资讯，以下是精选回顾：\n\n"

            # 按内容类型统计
            category_stats = self._analyze_news_categories(monthly_news)
            summary += "**分类总结：**\n"

            category_names = {
                'product': '📱 产品发布',
                'research': '🔬 技术进展',
                'policy': '📋 政策动态',
                'funding': '💰 资本动态',
                'competition': '🏆 市场竞争'
            }

            for category, count in category_stats.items():
                if count > 0:
                    summary += f"{category_names.get(category)}: {count}条\n"

            summary += "\n"

            # 热点话题分析
            hotspots = self._extract_hot_topics(monthly_news)
            if hotspots:
                summary += "**本月热点：**\n"
                for topic, info in hotspots.items():
                    summary += f"🌟 **{topic}**: {info['count']}次提及 - {info['description']}\n"
                summary += "\n"

            # 重大事件回顾
            major_events = self._identify_major_events(monthly_news)
            if major_events:
                summary += "**重大事件：**\n"
                for i, event in enumerate(major_events[:5], 1):
                    summary += f"{i}. {event['title']}\n"
                    summary += f"   时间：{event['date']}\n"
                    summary += f"   [详情]({event['link']})\n\n"

            # 发展趋势总结
            trend_insights = self._generate_trend_insights(monthly_news)
            summary += f"**趋势观察：**\n{trend_insights}\n\n"

            # 下月展望
            summary += "**下月看点：**\n"
            summary += "🔮 元旦假期后的AI行业复苏\n"
            summary += "📈 年度报告发布季即将到来\n"
            summary += "🎯 各公司Q4季度成果集中展示\n\n"

            summary += datetime.now().strftime("📅 报告生成：%Y-%m-%d")

            self.save_monthly_data(summary, monthly_news)
            return summary

        except Exception as e:
            error_msg = f"生成月总结失败: {str(e)}"
            print(error_msg)
            return error_msg

    def _generate_default_monthly_report(self) -> str:
        """生成默认的月度报告（当没有历史数据时）"""
        current_month = datetime.now().strftime('%Y年%m月')

        summary = f"📊 **{current_month} AI大盘点**\n\n"

        summary += """
欢迎来到本月AI行业总结！由于我们是第一次运行，还没有收集到完整的历史数据。

**现在可以做的事情：**
1. 📚 **浏览历史要闻**：查看科技媒体的月度总结
2. 🚀 **关注前沿动态**：机器之心、量子位等中文媒体
3. 💡 **了解行业趋势**：GitHub Trend、Hacker News等技术社区

**本月重点观察方向：**
📱 **大模型应用**：ChatGPT、Claude等的新功能
🤖 **AI工具爆发**：新的AI绘画、写作工具
🔬 **技术突破**：新算法、新架构的发布
💰 **投资动态**：AI创企的融资消息

下次月底将为您提供更完整的分析报告！

📅 让我们下个月见！
"""
        return summary

    def _analyze_news_categories(self, news_list: List[Dict[str, Any]]) -> Dict[str, int]:
        """分析新闻分类"""
        categories = {'product': 0, 'research': 0, 'policy': 0, 'funding': 0, 'competition': 0}

        for news in news_list:
            category = news.get('category', 'product')
            if category in categories:
                categories[category] += 1
            else:
                categories['product'] += 1

        return categories

    def _extract_hot_topics(self, news_list: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """提取热点话题"""
        all_titles = [news.get('title', '') for news in news_list]
        all_text = ' '.join(all_titles).lower()

        # 预定义的热点词汇
        topic_keywords = {
            '大模型': ['大模型', '大语言模型', 'llm'],
            'ChatGPT': ['chatgpt', 'gpt-4', 'gpt-3.5'],
            'AI绘画': ['ai绘画', 'stable diffusion', 'midjourney'],
            '机器人': ['机器人', 'robot', '自动化'],
            '自动驾驶': ['自动驾驶', '无人驾驶', 'autonomous'],
            'AIGC': ['aigc', 'generative ai', '生成式'],
            '融资': ['融资', 'funding', 'invest'],
            '开源': ['开源', 'open source', 'github']
        }

        hot_topics = {}
        for topic, keywords in topic_keywords.items():
            count = sum(1 for keyword in keywords if keyword in all_text)
            if count >= 1:
                description = self._get_topic_description(topic, count)
                hot_topics[topic] = {
                    'count': count,
                    'description': description
                }

        return dict(list(hot_topics.items())[:4])  # 取前4个热点

    def _get_topic_description(self, topic: str, count: int) -> str:
        """根据主题和频次生成描述"""
        descriptions = {
            '大模型': '技术大爆发的主要推动力',
            'ChatGPT': '持续霸屏的话题焦点',
            'AI绘画': '创意工具的重要分支',
            '机器人': '实体AI应用的代表',
            '自动驾驶': '落地应用的关键场景',
            'AIGC': '内容生产的革命性变革',
            '融资': '资本持续看好行业前景',
            '开源': '技术共享推动行业进步'
        }
        return descriptions.get(topic, f"热度{item: 高, 中, 低}[count//3]")

    def _identify_major_events(self, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """识别重大事件"""
        # 根据标题长度和特定关键词来判断重要性
        major_events = []

        for news in news_list:
            title = news.get('title', '')

            # 重大事件的判断标准
            importance_keywords = ['发布', '推出', '首次', '突破', '重大', '全球','中国', 'Meta', 'OpenAI', '百度', '谷歌', '微软']

            importance_score = 0
            for keyword in importance_keywords:
                if keyword in title:
                    importance_score += 1

            if len(title) > 15 or importance_score >= 2:
                # 格式化日期
                date_str = news.get('published', '')
                try:
                    if isinstance(date_str, str) and 'T' in date_str:
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        date_obj = datetime.now()
                    formatted_date = date_obj.strftime('%m月%d日')
                except:
                    formatted_date = datetime.now().strftime('%m月%d日')

                major_events.append({
                    'title': title,
                    'link': news.get('link', '#'),
                    'date': formatted_date,
                    'score': importance_score
                })

        # 按重要性排序，只保留最重要的
        major_events.sort(key=lambda x: x['score'], reverse=True)
        return major_events

    def _generate_trend_insights(self, news_list: List[Dict[str, Any]]) -> str:
        """生成趋势洞察"""
        if not news_list:
            return "本月没有太多动态，可能是行业在积蓄力量，下个月值得期待！"

        # 基于新闻数量和类型的简单分析
        total = len(news_list)

        if total > 20:
            return "本月AI行业活跃度很高，各条战线都在快速发展，预示着明年将迎来更大爆发。"
        elif total > 10:
            return "行业稳步发展，重要进展不断涌现，整体向好态势明显。"
        else:
            return "虽然规模不大，但每条都很关键，体现了质量优于数量的发展趋势。"

    def save_monthly_data(self, summary: str, news_list: List[Dict[str, Any]]):
        """保存月度数据"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)

            month_key = datetime.now().strftime('%Y-%m')
            monthly_data = {
                'month': month_key,
                'summary': summary,
                'total_news': len(news_list),
                'categories': self._analyze_news_categories(news_list),
                'timestamp': datetime.now().isoformat()
            }

            with open(f'{self.data_dir}/monthly_summary.json', 'w', encoding='utf-8') as f:
                json.dump(monthly_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"保存月度数据失败: {e}")

if __name__ == "__main__":
    generator = MonthlySummaryGenerator()
    summary = generator.generate_monthly_summary()
    print(summary)