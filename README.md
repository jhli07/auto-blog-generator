# 🤖 Auto Blog Generator

自动博客生成系统 - 用 AI 自动生成高质量技术博客文章

## ✨ 特性

- 🚀 **一键生成** - 根据话题自动生成 Markdown 文章
- 🤖 **多 AI 支持** - 支持 OpenAI API 和免费模板模式
- 📝 **批量生成** - 一次生成多篇文章
- 📤 **多平台发布** - 支持 Medium、WordPress
- 🎯 **话题推荐** - 内置热门技术话题库
- 💾 **本地存储** - JSON + Markdown 双格式保存

## 📦 安装

```bash
git clone https://github.com/jhli07/auto-blog-generator.git
cd auto-blog-generator
pip install openai anthropic
```

## 🔧 配置

### 环境变量

```bash
# OpenAI (可选)
export OPENAI_API_KEY="your-api-key"

# Medium (可选)
export MEDIUM_TOKEN="your-medium-integration-token"

# WordPress (可选)
export WORDPRESS_URL="https://your-site.com"
export WORDPRESS_USER="username"
export WORDPRESS_PASS="password"
```

## 🚀 使用

### 基本使用

```bash
python auto_blog.py
```

### Python API

```python
from auto_blog import ContentGenerator, OpenAIProvider, FreeProvider

# 使用免费模板生成
provider = FreeProvider()
generator = ContentGenerator(provider)

# 生成单篇文章
post = generator.generate_post("Python 自动化技巧", ["Python", "自动化"])

# 生成系列文章
posts = generator.generate_series([
    "Python 入门教程",
    "Python 进阶技巧",
    "Python 项目实战"
])

# 保存文章
generator.save_posts("posts.json")
generator.export_markdown("my_posts")
```

### 发布到 Medium

```python
from auto_blog import BlogPublisher

publisher = BlogPublisher()
results = publisher.publish_all(generator.posts)
```

## 📁 输出格式

### posts.json

```json
{
  "generated_at": "2025-02-25T14:00:00",
  "total_posts": 3,
  "posts": [
    {
      "title": "详解 Python 自动化技巧",
      "content": "...",
      "tags": ["Python", "自动化"],
      "status": "draft",
      "word_count": 1200,
      "read_time_minutes": 6
    }
  ]
}
```

### Markdown 文件

自动生成规范的 Markdown 文件，可直接导入到任何博客平台。

## 🎯 变现思路

### 1. Medium Partner Program
- 发布文章 → 获取付费阅读收入
- 预计收益：$0.01 - $10/篇/月

### 2. 联盟营销
- 在文章中插入工具/课程链接
- 读者购买 → 获取佣金

### 3. 付费订阅
- 优质内容 → 邮件订阅
- 定期发送专属文章

### 4. 内容打包
- 整理合集 → 打包出售
- 例如：《Python 自动化实战电子书》

## 📊 收益预期

| 策略 | 月收入预估 | 投入时间 |
|------|-----------|---------|
| Medium 广告 | $50-200 | 每周 2 小时 |
| 联盟营销 | $100-500 | 每周 3 小时 |
| 付费订阅 | $200-1000 | 每周 5 小时 |

## 🔒 注意事项

1. **版权问题**：AI 生成内容需人工审核和修改
2. **平台规则**：注意各平台的原创度要求
3. **质量控制**：建议人工润色后再发布
4. **频率控制**：不要过度发布，保持质量

## 📝 许可证

MIT License

## 🤝 贡献

欢迎 PRs 和 Issues！

---

*Built with ❤️ by Agent_Li*
