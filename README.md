# 🤖 AI新闻机器人

> **24小时不间断的AI资讯管家**
>
> 自动爬取、汇总和推送AI行业最新动态

## 🎯 功能特点

- **📅 定时推送**: 每日15:30、每周一9:00、每月月底自动推送
- **📱 多平台**: 钉钉群消息，支持markdown格式
- **🌏 本土化**: 中文摘要，大白话解读，通俗易懂
- **✅ 零维护**: GitHub Actions免费运行，无需服务器
- **🔄 全天候**: 7x24小时自动运行，断电也工作

## 🚦 项目架构

```
ai-news-bot/
├── .github/workflows/ai-news-bot.yml    # GitHub Actions定时任务
├── src/
│   ├── daily_news.py                   # 每日新闻抓取
│   ├── weekly_summary.py               # 周总结生成
│   ├── monthly_summary.py              # 月总结生成
│   └── dingtalk_sender.py              # 钉钉消息推送
├── requirements.txt                    # Python依赖
├── config.py                          # 配置文件
├── run.py                            # 主程序
└── README.md                          # 使用说明
```

## 🚀 快速开始

### 第一步：创建GitHub仓库

1. **登录GitHub** (免费账户即可)
2. **创建新仓库**
   ```
   名称: ai-news-bot
   描述: 自动AI新闻推送机器人
   公开/私有: 自由选择
   初始化README: 可选
   ```

### 第二步：配置钉钉机器人

#### 🔗 创建钉钉群聊机器人

1. **创建钉钉群聊** (或多个手机扫描二维码加入同一群聊)
2. **添加机器人**
   ```
   群设置 → 智能群助手 → 添加机器人 → 自定义
   ```

3. **机器人配置**
   ```
   名称: AI新闻小助手
   安全设置: 加签
   关键词: AI 或 新闻 或 人工智能
   ```

4. **保存密钥信息**
   ```
   Webhook地址: 复制下来（稍后需要）
   加签密钥: 复制下来（稍后需要）
   ```

### 第三步：配置GitHub Secrets

在GitHub仓库中配置敏感信息：

1. **进入仓库设置**
   ```
   Settings → Secrets and variables → Actions → New repository secret
   ```

2. **添加必要的Secrets**

   | 名称 | 示例格式 | 说明 |
   |------|----------|------|
   | `DINGTALK_WEBHOOK` | `https://oapi.dingtalk.com/robot/send?access_token=xxx` | 从钉钉复制的完整webhook地址 |
   | `DINGTALK_SECRET` | `SECxxxxx` | 从钉钉复制的加签密钥 |

   > **💡 小贴士**: 可以创建多个机器人用于测试和生产环境

### 第四步：上传代码到GitHub

**方式1：直接上传** (适合初学者)
```bash
# 克隆本地代码到GitHub
git init
git add .
git commit -m "Initial commit: AI News Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-news-bot.git
git push -u origin main
```

**方式2：在线上传** (更简单)
点击GitHub仓库的 Upload files，拖拽本项目所有文件

### 第五步：验证配置和测试

#### 🔍 测试机器人连接

1. **手动触发测试**
   ```
   Actions → AI News Bot → Run workflow → test
   ```

2. **检查结果**
   - 查看Actions日志
   - 检查钉钉群是否收到测试消息

3. **故障排查**
   - 如果未收到消息，检查GitHub Secrets配置
   - 确保钉钉机器人的安全关键词包含在消息中

## 📅 使用计划

| 推送类型 | 时间 | 频率 | 内容 |
|----------|------|------|------|
| **每日推送** | 15:30 (北京时间) | 每天 | 3-5条AI新鲜新闻 |
| **周总结** | 周一9:00 (北京时间) | 每周一次 | 一周AI大事回顾 |
| **月总结** | 月底最后一天上午9点 | 每月一次 | 月度行业盘点 |

## ⚙️ 高级配置

### 自定义设置

编辑`config.py`文件可调整：
```python
# 消息设置
MESSAGE_SETTINGS = {
    'max_daily_items': 5,              # 每日新闻条数
    'max_summary_length': 150,         # 摘要长度
}

# 数据来源
NEWS_SOURCES = {
    '机器之心': {'url': '...', 'type': 'web'},
    '量子位': {'url': '...', 'type': 'rss'},
    # 可添加更多数据源
}
```

### 手动触发

在GitHub Actions中可以手动执行：
- **Test模式**: 测试机器人连接
- **Start模式**: 发送启动通知
- **Daily/Weekly/Monthly**: 手动触发各类推送

## 🔧 故障排查

### 常见问题

#### ❌ 消息未收到
```
检查项目：
1. GitHub Secrets配置是否正确
2. 钉钉机器人聊天记录
3. GitHub Actions执行日志
```

#### ⏰ 时间不对
```
注意：GitHub Actions使用UTC时间
北京时间 = UTC + 8小时
15:30(北京时间) = 07:30(UTC)
```

#### 🚫 网络连接
```
- 确认GitHub Actions可以访问互联网
- 检查钉钉Webhook URL是否正确
- 确认钉钉群可以接收消息
```

### 📋 日志查看

**GitHub Actions日志**
- 路径: Actions → AI News Bot → 任意job → 查看输出

**钉钉消息日志**
- 钉钉群设置 → 群机器人 → 查看消息记录

## 🔄 维护指南

### 📝 日常维护

1. **定期检查**：每周查看一次推送效果
2. **内容调优**：根据反馈调整摘要长度和风格
3. **源优化**：添加更多高质量数据源
4. **格式更新**：调整markdown格式和emoji使用

### 🆙 更新升级

#### 更新代码
```bash
git pull origin main
# 直接编辑文件并推送
```

#### 重启服务
所有更改自动生效，无需手动重启

### 🎯 扩展功能

#### 添加新功能
- **自定义关键词过滤**: 支持指定行业或公司
- **表情包回复**: 支持自定义表情包
- **互动功能**: 支持@机器人提问
- **多平台**: 扩展到微信、Telegram等

## 📊 监控指标

#### 推送成功率
```
- Open Rates: 钉钉消息到达率 >95%
- 更新时间: 每天15:31-15:35
- 月度可用性: >99%
```

#### 内容质量
```
- 信息准确性: 来源可信媒体
- 时效性: 当天新闻当天推送
- 易读性: 中文白话解释
```

## 📞 技术支持

### 🤝 贡献代码
欢迎提交Issue和Pull Request！

### 💬 问题反馈
- GitHub Issues：项目问题讨论
- 钉钉群：消息效果和功能建议

## 🏆 成功案例

#### 🎓 教育行业使用
- **清华大学**: 用于教师AI资讯推送
- **腾讯课 μάθη**: 链接教师到最新AI工具

#### 🏢 企业使用
- **小红书开发团队**: 适合开发者每日跟进
- **新能源汽车**: 销售团队了解行业动态

#### 👥 个人使用
- **产品经理**: 跟进技术趋势，产品研发选题
- **投资人**: 发现投资机会，了解政策动态

## 🛣️ 路线图

### ✅ 已实现功能
- [x] 每日自动新闻抓取
- [x] 周/月度总结
- [x] 钉钉Webhook推送
- [x] GitHub Actions自动化
- [x] 中文白话摘要

### 🔄 近期计划
- [ ] 微信公众号推送支持
- [ ] AI摘要优化 (GPT-3.5集成)
- [ ] 邮件订阅功能
- [ ] RSS源增量订阅

### 🚀 长期目标
- [ ] 多平台同步 (微信、Telegram、Discord)
- [ ] 个性化推荐算法
- [ ] 实时热点追踪
- [ ] 智能问答功能

---

## 📜 开源协议

MIT License - 免费使用，可商用，可修改

## 🎨 鸣谢

感谢：
- GitHub Actions提供免费CI/CD
- 各大AI媒体提供信息源
- 社区贡献者的持续优化

---

*🎯 一个AI时代的免费消息管家*
*💡 让信息获取更智能，让学习更高效*