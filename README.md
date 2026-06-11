# 每日新闻推送系统

自动获取经济政策和电力行业新闻，通过AI生成个性化摘要，每天早上推送到企业微信。

## 功能特性

- ✅ 自动获取经济政策新闻
- ✅ 自动获取电力行业新闻
- ✅ AI生成个性化摘要（小米MiMo）
- ✅ 企业微信应用消息推送
- ✅ 每天定时运行（北京时间8:00）
- ✅ 完全免费（GitHub Actions）

## 快速开始

### 1. Fork 本项目

点击右上角的 "Fork" 按钮，将项目复制到你的GitHub账号。

### 2. 配置 Secrets

进入你Fork的仓库，点击 **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下4个Secret：

| Secret名称 | 说明 | 示例 |
|------------|------|------|
| `WECHAT_CORPID` | 企业微信企业ID | `wwbc0f0845a3ec6f65` |
| `WECHAT_CORPSECRET` | 企业微信应用Secret | `751zWpNGDcOhk9qbUk6_jf...` |
| `WECHAT_AGENTID` | 企业微信应用AgentId | `1000002` |
| `AI_API_KEY` | 小米MiMo API Key | `sk-cbhzlcpncyjanfizvjw...` |

### 3. 启用 GitHub Actions

进入 **Actions** 选项卡，点击 "I understand my workflows, go ahead and enable them"。

### 4. 测试运行

点击 **Actions** → **每日新闻推送** → **Run workflow** → **Run workflow** 手动触发一次测试。

### 5. 等待定时任务

配置完成后，系统会在每天北京时间早上8:00自动运行。

## 工作原理

```
GitHub Actions（定时触发）
    ↓
Python脚本执行：
├── 1. 获取经济政策新闻
├── 2. 获取电力行业新闻
├── 3. 调用小米MiMo生成AI摘要
└── 4. 调用企业微信API推送
    ↓
企业微信收到消息
```

## 项目结构

```
daily-news-push/
├── .github/
│   └── workflows/
│       └── daily-push.yml    # GitHub Actions工作流配置
├── scripts/
│   ├── fetch_news.py         # 新闻获取模块
│   ├── generate_summary.py   # AI摘要生成模块
│   ├── send_wechat.py        # 企业微信发送模块
│   └── main.py               # 主程序
├── config.json               # 配置文件（本地测试用）
├── requirements.txt          # Python依赖
└── README.md                 # 本文件
```

## 自定义配置

### 修改新闻关键词

编辑 `scripts/main.py` 中的 `load_config` 函数：

```python
config = {
    # ...
    "news": {
        "keywords": ["经济政策", "电力行业", "新能源", "电力市场", "能源改革"],
        "max_articles": 5
    }
}
```

### 修改推送时间

编辑 `.github/workflows/daily-push.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '30 23 * * *'  # UTC时间23:30 = 北京时间7:30
```

**时间转换公式：** 北京时间 = UTC时间 + 8小时

例如：
- 北京时间 8:00 = UTC 0:00 → `cron: '0 0 * * *'`
- 北京时间 7:30 = UTC 23:30 → `cron: '30 23 * * *'`
- 北京时间 9:00 = UTC 1:00 → `cron: '0 1 * * *'`

### 修改AI模型

编辑 `.github/workflows/daily-push.yml` 中的环境变量：

```yaml
env:
  AI_API_ENDPOINT: 'https://api.xiaomimimo.com/v1/chat/completions'
  AI_MODEL: 'MiMo'  # 修改为其他模型名称
```

## 常见问题

### Q: 如何验证配置是否正确？

A: 手动触发一次工作流（Actions → Run workflow），查看运行日志。

### Q: 消息发送失败怎么办？

A: 检查以下几点：
1. 企业微信凭证是否正确
2. 企业微信应用是否启用
3. 应用可见范围是否包含你自己

### Q: 如何添加更多新闻源？

A: 编辑 `scripts/fetch_news.py`，在 `main` 函数中添加新的新闻获取逻辑。

### Q: 如何停止推送？

A: 进入 **Settings** → **Actions** → **General**，选择 "Disable actions"。

## API参考

### 企业微信API文档
- 官方文档：https://developer.work.weixin.qq.com/document/path/90236

### 小米MiMo API文档
- 平台地址：https://platform.xiaomimimo.com

## 许可证

MIT License

## 支持

如有问题，请提交 Issue。
