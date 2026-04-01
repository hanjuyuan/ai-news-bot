# 🤖 AI新闻机器人 - 优化版配置文件
import os

# 1. 钉钉机器人配置
# 这里的 Webhook 和 Secret 会自动从 GitHub 的 Secrets 环境变量中读取
DINGTALK_WEBHOOK = os.getenv('DINGTALK_WEBHOOK', '')
DINGTALK_SECRET = os.getenv('DINGTALK_SECRET', '')

# 2. 新闻数据源配置 (已优化为高稳定性中文 RSS 源)
NEWS_SOURCES = {
    'jiqizhixin': {
        'name': '机器之心',
        'url': 'https://www.jiqizhixin.com/rss',
        'type': 'rss'
    },
    '36kr_ai': {
        'name': '36Kr-AI频道',
        'url': 'https://36kr.com/feed-newsfeed/208',
        'type': 'rss'
    },
    'ithome_ai': {
        'name': 'IT之家-人工智能',
        'url': 'https://www.ithome.com/rss/',
        'type': 'rss'
    },
    # 如果您需要看国外前沿资讯，可以保留下面两个（内容会是英文）
    # 如果只想要纯中文，可以将下面两个源用 # 号注释掉
    'openai_blog': {
        'name': 'OpenAI Blog',
        'url': 'https://openai.com/blog/rss.xml',
        'type': 'rss'
    },
    'techcrunch_ai': {
        'name': 'TechCrunch AI',
        'url': 'https://techcrunch.com/category/artificial-intelligence/feed/',
        'type': 'rss'
    }
}

# 3. 消息推送配置
MESSAGE_SETTINGS = {
    'max_daily_items': 5,              # 每日新鲜事推送条数
    'max_summary_length': 150,         # 每条新闻摘要的字数限制
    'emoji_map': {                     # 用于 Markdown 的精美图标
        'product': '📱',
        'research': '🔬',
        'policy': '📋',
        'funding': '💰',
        'competition': '🏆',
        'default': '🚀'
    }
}

# 4. 运行环境配置
TIMEZONE = 'Asia/Shanghai'            # 统一使用北京时间

# 5. 文件存储路径 (GitHub Actions 环境下会自动创建)
DATA_DIR = 'data'
DAILY_NEWS_FILE = f'{DATA_DIR}/daily_news.json'
WEEKLY_NEWS_FILE = f'{DATA_DIR}/weekly_news.json'
MONTHLY_NEWS_FILE = f'{DATA_DIR}/monthly_news.json'
