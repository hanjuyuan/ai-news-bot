#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻机器人主程序
运行入口，支持多种操作模式
"""

import argparse
import sys
import os
from datetime import datetime

# 添加项目根目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.daily_news import DailyNewsScraper
from src.weekly_summary import WeeklySummaryGenerator
from src.monthly_summary import MonthlySummaryGenerator
from src.dingtalk_sender import DingTalkSender

def main():
    parser = argparse.ArgumentParser(description='AI新闻机器人')
    parser.add_argument('action', choices=['daily', 'weekly', 'monthly', 'test', 'startup'],
                       help='选择要执行的操作')
    parser.add_argument('--dry-run', action='store_true',
                       help='干运行模式，不实际发送消息')
    parser.add_argument('--quiet', action='store_true',
                       help='静默模式，减少输出')

    args = parser.parse_args()

    sender = DingTalkSender()

    # 验证配置
    config_result = sender.validate_config()
    if not config_result['is_valid']:
        print("❌ DingTalk配置无效:")
        print(f"   Webhook配置: {config_result['webhook_configured']}")
        print(f"   URL格式正确: {config_result['webhook_url_format']}")
        print("   请检查环境变量 DINGTALK_WEBHOOK 和 DINGTALK_SECRET")
        sys.exit(1)

    if not args.quiet:
        print("🚀 AI新闻机器人启动")
        print(f"   操作: {args.action}")
        print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        if args.action == 'daily':
            scraper = DailyNewsScraper()
            content = scraper.get_daily_news_summary()

            if args.dry_run:
                print("\n=== 每日新闻预览 ===")
                print(content)
            else:
                result = sender.send_daily_news(content)
                if not args.quiet:
                    print(f"发送结果: {result}")

        elif args.action == 'weekly':
            generator = WeeklySummaryGenerator()
            content = generator.generate_weekly_summary()

            if args.dry_run:
                print("\n=== 周总结预览 ===")
                print(content)
            else:
                result = sender.send_weekly_summary(content)
                if not args.quiet:
                    print(f"发送结果: {result}")

        elif args.action == 'monthly':
            generator = MonthlySummaryGenerator()
            content = generator.generate_monthly_summary()

            if args.dry_run:
                print("\n=== 月总结预览 ===")
                print(content)
            else:
                result = sender.send_monthly_summary(content)
                if not args.quiet:
                    print(f"发送结果: {result}")

        elif args.action == 'test':
            print("🔍 测试连接...")
            result = sender.test_connection()
            print(f"测试结果: {result}")

        elif args.action == 'startup':
            print("📱 发送启动通知...")
            result = sender.send_startup_message()
            print(f"启动通知结果: {result}")

        if not args.quiet:
            print("✅ 任务完成")

    except Exception as e:
        print(f"❌ 执行失败: {e}")
        # 尝试发送错误通知
        try:
            sender.send_error_message("执行失败", str(e))
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()