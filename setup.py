#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻机器人设置向导
交互式设置向导，帮助用户配置机器人
"""

import os
import json
import sys


def setup_wizard():
    """交互式设置向导"""
    print("🎉 AI新闻机器人设置向导")
    print("=" * 50)

    print("\n📋 欢迎使用AI新闻机器人设置向导！")
    print("我将帮助您完成以下配置：")
    print("1. 🎯 创建钉钉机器人")
    print("2. ⚙️ 配置GitHub Secrets")
    print("3. 🧪 测试连接")
    print("4. ✅ 验证配置")

    input("\n按Enter开始设置...")

    print("\n" + "="*50)
    print("🎯 第一步：创建钉钉机器人")
    print("="*50)

    print("\n" + " 📱 钉钉机器人创建步骤:")
    print("1. 打开钉钉手机APP")
    print("2. 创建或进入一个已有群聊")
    print("3. 点击右上角三个点 → 群设置")
    print("4. 下拉找到“智能群助手” → 添加机器人")
    print("5. 选择“自定义”机器人")
    print("6. 填写以下信息：")
    print("   - 机器人名称：AI新闻小助手")
    print("   - 安全设置：加签")
    print("   - 关键词：AI 或 新闻")

    webhook = input('\n请输入钉钉的Webhook URL: ').strip()
    secret = input('请输入钉钉的加签密钥: ').strip()

    # 创建.env.example文件
    config_content = f"""
# 钉钉配置示例
# 请将以下内容复制到GitHub Secrets中

DINGTALK_WEBHOOK={webhook}
DINGTALK_SECRET={secret}
"""

    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(config_content)

    print("\n✅ 配置信息已保存到 .env.example")

    print("\n" + "="*50)
    print("⚙️ 第二步：配置GitHub Secrets")
    print("="*50)

    print("\n" + " 🔗 GitHub Secrets设置步骤:")
    print("1. 打开您的GitHub仓库")
    print("2. 点击 Settings → Secrets and variables → Actions")
    print("3. 点击 New repository secret")
    print("4. 配置两个必需的项目：")

    print(f"\n   添加DINGTALK_WEBHOOK:")
    print(f"   Name: DINGTALK_WEBHOOK")
    print(f"   Value: {webhook}")

    print(f"\n   添加DINGTALK_SECRET:")
    print(f"   Name: DINGTALK_SECRET")
    print(f"   Value: {secret}")

    input("\n按Enter继续...")

    print("\n" + "="*50)
    print("🧪 第三步：测试连接")
    print("="*50)

    test_choice = input("\n是否现在测试连接？ (y/n): ").lower()

    if test_choice == 'y':
        print("\n🔄 正在测试钉钉连接...")

        # 保存测试环境
        os.environ['DINGTALK_WEBHOOK'] = webhook
        os.environ['DINGTALK_SECRET'] = secret

        try:
            from src.dingtalk_sender import DingTalkSender

            sender = DingTalkSender()
            result = sender.test_connection()

            if result.get('success'):
                print("\n✅ 连接测试成功！")
                print("   您的钉钉群应该收到了测试消息")
            else:
                print(f"\n❌ 连接测试失败: {result.get('error')}")
                print("   请检查：")
                print("   1. 钉钉URL和密钥是否正确")
                print("   2. 网络连接是否正常")
                print("   3. 机器人是否有相应权限")

        except Exception as e:
            print(f"\n❌ 测试时出现错误: {e}")

    print("\n" + "="*50)
    print("📚 使用指南")
    print("="*50)

    print("\n" + " 🚀 接下来的步骤:")
    print("1. 上传代码到GitHub")
    print("2. 等待第一次自动执行")
    print("3. 手动触发测试 (可选)")

    print("\n" + " 📅 时间安排:")
    print("• 每日推送: 15:30 北京时间")
    print("• 每周总结: 周一 9:00 北京时间")
    print("• 每月总结: 月底最后一天")

    print("\n" + " ⚡ 手动触发方式:")
    print("GitHub → Actions → AI News Bot → Run workflow")
    print("选择: test/daily/weekly/monthly")

    print("\n" + "🎉 设置完成！")
    print("="*50)
    print("使用愉快！任何问题请查看README.md或提Issue")

if __name__ == "__main__":
    setup_wizard()