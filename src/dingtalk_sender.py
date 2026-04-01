#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉消息发送模块
通过Webhook将AI新闻推送到钉钉群
"""
from typing import Dict, Any
import requests
import json
import time
import hashlib
import hmac
import base64
import urllib.parse
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DINGTALK_WEBHOOK, DINGTALK_SECRET

class DingTalkSender:
    def __init__(self):
        self.webhook_url = DINGTALK_WEBHOOK
        self.secret = DINGTALK_SECRET
        self.max_retries = 3
        self.timeout = 30

    def _generate_sign(self, timestamp: str) -> str:
        """生成钉钉签名"""
        if not self.secret:
            return ""

        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_message(self, content: str, message_type: str = "markdown") -> Dict:
        """发送消息到钉钉"""
        if not self.webhook_url:
            return {"errcode": 400, "errmsg": "钉钉Webhook URL未配置"}

        try:
            timestamp = str(round(time.time() * 1000))
            sign = self._generate_sign(timestamp)

            # 构建完整的URL
            url = self.webhook_url
            if self.secret:
                url += f"&timestamp={timestamp}&sign={sign}"

            if message_type == "markdown":
                data = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": "AI新闻推送",
                        "text": content
                    }
                }
            else:
                data = {
                    "msgtype": "text",
                    "text": {
                        "content": content
                    }
                }

            headers = {'Content-Type': 'application/json'}

            for attempt in range(self.max_retries):
                try:
                    response = requests.post(
                        url,
                        data=json.dumps(data, ensure_ascii=False),
                        headers=headers,
                        timeout=self.timeout
                    )
                    result = response.json()

                    if result.get("errcode") == 0:
                        print(f"钉钉消息发送成功")
                        return {"success": True, "result": result}
                    else:
                        print(f"钉钉消息发送失败: {result}")
                        if attempt < self.max_retries - 1:
                            time.sleep(2 ** attempt)  # 指数退避
                        else:
                            return {"success": False, "error": result}

                except requests.exceptions.Timeout:
                    print(f"钉钉请求超时 (尝试 {attempt + 1}/{self.max_retries})")
                    if attempt == self.max_retries - 1:
                        return {"success": False, "error": "请求超时"}
                    time.sleep(2 ** attempt)

                except requests.exceptions.RequestException as e:
                    print(f"钉钉请求异常 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                    if attempt == self.max_retries - 1:
                        return {"success": False, "error": str(e)}
                    time.sleep(2 ** attempt)

        except Exception as e:
            error_msg = f"发送钉钉消息错误: {e}"
            print(error_msg)
            return {"success": False, "error": error_msg}

    def send_daily_news(self, daily_news_reslut: str) -> Dict:
        """发送每日新闻"""
        title = "📰 今日AI新鲜事"
        content = daily_news_reslut
        return self.send_message(content, "markdown")

    def send_weekly_summary(self, weekly_summary: str) -> Dict:
        """发送周总结"""
        title = "🗓️ 本周AI大盘点"
        content = weekly_summary
        return self.send_message(content, "markdown")

    def send_monthly_summary(self, monthly_summary: str) -> Dict:
        """发送月总结"""
        title = "📊 本月AI大盘点"
        content = monthly_summary
        return self.send_message(content, "markdown")

    def send_error_message(self, error_type: str, error_detail: str) -> Dict:
        """发送错误信息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"⚠️ **AI新闻机器人告警**\n\n"
        content += f"❌ 错误类型：{error_type}\n"
        content += f"📄 详细信息：{error_detail}\n"
        content += f"🕒 发生时间：{timestamp}\n\n"
        content += "请检查机器人配置和网络连接。\n"

        return self.send_message(content, "markdown")

    def test_connection(self) -> Dict:
        """测试钉钉连接"""
        test_content = "🤖 **AI新闻机器人测试消息**\n\n"
        test_content += "✅ 连接测试成功！\n"
        test_content += "机器人已正确配置，可以开始接收AI新闻推送。\n\n"
        test_content += "下一步设置工作：\n"
        test_content += "1. 📅 配置定时任务 (GitHub Actions)\n"
        test_content += "2. 🎛️ 根据您的需求调整推送频率\n"
        test_content += "3. 📱 开始使用并接收AI资讯\n\n"
        test_content += datetime.now().strftime("📷 测试时间：%Y-%m-%d %H:%M:%S")

        return self.send_message(test_content, "markdown")

    def send_startup_message(self) -> Dict:
        """发送启动消息"""
        welcome_content = "🎉 **AI新闻机器人上线啦！**\n\n"
        welcome_content += "📰 **功能介绍**\n"
        welcome_content += "- 每日15:30自动推送当天AI新鲜事\n"
        welcome_content += "- 每周一早9:00推送周总结\n"
        welcome_content += "- 每月最后一天推送月度盘点\n"
        welcome_content += "- 内容涵盖产品发布、技术突破、行业动态等\n\n"

        welcome_content += "🎯 **内容特色**\n"
        welcome_content += "- 中文大白话，易读易懂\n"
        welcome_content += "- 精选高质量信息，拒绝垃圾内容\n"
        welcome_content += "- 来源权威，覆盖机器之心、量子位、36氪等\n\n"

        welcome_content += "⚙️ **使用说明**\n"
        welcome_content += "- 完全免费，24小时自动运行\n"
        welcome_content += "- 可在GitHub Actions中手动触发测试\n"
        welcome_content += "- 后续可扩展更多平台\n\n"

        welcome_content += "🚀 让我们开始AI资讯之旅吧！\n\n"
        welcome_content += datetime.now().strftime("🎈 启动时间：%Y-%m-%d %H:%M:%S")

        return self.send_message(welcome_content, "markdown")

    def validate_config(self) -> Dict:
        """验证钉钉配置"""
        validation_result = {
            "webhook_configured": bool(self.webhook_url),
            "secret_configured": bool(self.secret),
            "webhook_url_format": self.webhook_url.startswith("https://oapi.dingtalk.com/robot/send") if self.webhook_url else False
        }

        validation_result["is_valid"] = validation_result["webhook_configured"] and validation_result["webhook_url_format"]

        return validation_result

if __name__ == "__main__":
    # 测试配置
    sender = DingTalkSender()
    config_status = sender.validate_config()

    if config_status["is_valid"]:
        print("✅ 钉钉配置有效")
        # 发送测试消息
        test_result = sender.test_connection()
        print(f"测试结果: {test_result}")
    else:
        print("❌ 钉钉配置无效")
        print(f"配置状态: {config_status}")
        print("请检查 GitHub Secrets 中的以下配置：")
        print("- DINGTALK_WEBHOOK: 钉钉机器人的Webhook URL")
        print("- DINGTALK_SECRET: 钉钉机器人的加签密钥")
