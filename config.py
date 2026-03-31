# 配置文件
import os

# 钉钉机器人配置
DINGTALK_WEBHOOK = os.getenv('DINGTALK_WEBHOOK', '')
DINGTALK_SECRET = os.getenv('DINGTALK_SECRET', '')

# 新闻数据源
NEWS_SOURCES = {
    'jiqizhixin': {
        'url': 'https://www.jiqizhixin.com/articles',
        'type': 'rss'
    },
    '36kr_ai': {
        'url': 'https://36kr.com/search/articles/AI',
        'type': 'web'
    },
    'liangziwei': {
        'url': 'https://www.qbitai.com/category/ai',
        'type': 'web'
    },
    'openai_blog': {
        'url': 'https://openai.com/blog/rss.xml',
        'type': 'rss'
    },
    'techcrunch_ai': {
        'url': 'https://techcrunch.com/category/artificial-intelligence/feed/',
        'type': 'rss'
    }
}

# 消息配置
MESSAGE_SETTINGS = {
    'max_daily_items': 5,
    'max_summary_length': 150,
    'emoji_map': {
        'product': '📱',
        'research': '🔬',
        'policy': '📋',
        'funding': '💰',
        'competition': '🏆'
    }
}

# 时区配置
TIMEZONE = 'Asia/Shanghai'

# 文件存储路径
DATA_DIR = 'data'
DAILY_NEWS_FILE = f'{DATA_DIR}/daily_news.json'
WEEKLY_NEWS_FILE = f'{DATA_DIR}/weekly_news.json'
MONTHLY_NEWS_FILE = f'{DATA_DIR}/monthly_news.json'