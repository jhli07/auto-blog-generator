#!/usr/bin/env python3
"""
自动博客生成系统
Auto Blog Generator System
"""

import os
import json
import datetime
import random
from typing import List, Dict, Optional
from abc import ABC, abstractmethod

# 导入 provider
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


class BlogPost:
    """博客文章类"""
    
    def __init__(self, title: str, content: str, tags: List[str], platform: str = "medium"):
        self.title = title
        self.content = content
        self.tags = tags
        self.platform = platform
        self.created_at = datetime.datetime.now()
        self.status = "draft"
        self.word_count = len(content.split())
        self.read_time = self.word_count // 200  # 每分钟约200词
        
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "platform": self.platform,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "word_count": self.word_count,
            "read_time_minutes": self.read_time
        }


class AIProvider(ABC):
    """AI Provider 抽象基类"""
    
    @abstractmethod
    def generate_content(self, prompt: str, max_tokens: int = 1000) -> str:
        pass
    
    @abstractmethod
    def generate_title(self, topic: str) -> str:
        pass


class OpenAIProvider(AIProvider):
    """OpenAI Provider"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if self.api_key and HAS_OPENAI:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            
    def generate_content(self, prompt: str, max_tokens: int = 1500) -> str:
        if not self.client:
            return f"[需要 OpenAI API Key]\n\n{prompt}"
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的技术博客作者。写作用心、结构清晰、有深度。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"生成失败: {e}"
    
    def generate_title(self, topic: str) -> str:
        prompt = f"为一个关于'{topic}'的技术文章生成一个吸引人的标题。要求：简洁、有吸引力、包含关键词。"
        content = self.generate_content(prompt, max_tokens=100)
        return content.strip().strip('"').strip("'")


class FreeProvider(AIProvider):
    """免费 AI Provider (使用模拟或本地模型)"""
    
    def __init__(self, provider_type: str = "local"):
        self.provider_type = provider_type
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, dict]:
        return {
            "python": {
                "intro": "Python 作为当下最受欢迎的编程语言之一，",
                "outro": "希望这篇文章对你有帮助！如果你有任何问题，欢迎在评论区留言。"
            },
            "automation": {
                "intro": "自动化正在改变我们的工作方式。",
                "outro": "拥抱自动化，让生活更美好！"
            },
            "ai": {
                "intro": "人工智能技术日新月异，",
                "outro": "让我们一起探索 AI 的无限可能！"
            },
            "webdev": {
                "intro": "Web 开发是一个永不停歇的领域，",
                "outro": "持续学习是保持竞争力的关键。"
            }
        }
    
    def generate_content(self, prompt: str, max_tokens: int = 1500) -> str:
        """使用模板和关键词生成内容"""
        # 提取关键词
        keywords = self._extract_keywords(prompt)
        
        # 选择模板
        template = self._select_template(keywords)
        
        # 生成内容
        title = self.generate_title(prompt)
        
        content = f"""# {title}

{self._generate_intro(keywords)}

## 什么是 {keywords[0] if keywords else '这个技术'}？

{keywords[0] if keywords else '这个技术'} 是当今技术领域中一个非常重要的话题。它不仅改变了我们工作方式，也在不断推动创新。

## 主要特点

1. **高效性** - 能够大大提升我们的工作效率
2. **易用性** - 学习曲线平缓，容易上手
3. **可扩展性** - 可以根据需求灵活扩展

## 实际应用场景

{self._generate_use_cases(keywords)}

## 如何开始

如果你想学习 {keywords[0] if keywords else '这个技术'}，可以按照以下步骤：

1. **了解基础知识** - 先掌握核心概念
2. **动手实践** - 理论结合实际
3. **项目实战** - 通过项目巩固知识

## 常见问题 (FAQ)

**Q: 学习 {keywords[0] if keywords else '这个技术'} 需要多长时间？**
A: 因人而异，通常 1-3 个月可以入门。

**Q: 需要编程基础吗？**
A: 有基础会更容易上手，但没有也不是完全不行。

## 总结

{self._generate_summary(keywords)}

{template.get('outro', '希望对你有帮助！')}

---

*本文由 AI 自动生成 | 阅读时间约 {max_tokens // 200} 分钟*
"""
        return content
    
    def generate_title(self, topic: str) -> str:
        """生成标题"""
        templates = [
            f"详解{topic}：从入门到精通",
            f"为什么{topic}如此重要？",
            f"{topic}完全指南：2025年最新",
            f"掌握{topic)，看这一篇就够了",
            f"新手必看：{topic}入门教程"
        ]
        return random.choice(templates)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        tech_terms = ["python", "javascript", "react", "ai", "ml", "docker", 
                      "git", "linux", "api", "database", "web", "automation",
                      "chatgpt", "llm", "机器学习", "深度学习", "爬虫"]
        
        text_lower = text.lower()
        for term in tech_terms:
            if term in text_lower:
                keywords.append(term.title())
        return keywords if keywords else ["技术"]
    
    def _select_template(self, keywords: List[str]) -> dict:
        """选择模板"""
        for key in self.templates:
            if any(k.lower().startswith(key.lower()) for k in keywords):
                return self.templates[key]
        return random.choice(list(self.templates.values()))
    
    def _generate_intro(self, keywords: List[str]) -> str:
        """生成引言"""
        template = self._select_template(keywords)
        return template["intro"] + f"特别是在 {keywords[0] if keywords else '相关领域'] 方面。"
    
    def _generate_use_cases(self, keywords: List[str]) -> str:
        """生成使用场景"""
        cases = [
            f"• 数据分析和处理",
            f"• 自动化脚本编写",
            f"• Web 应用开发",
            f"• AI 模型训练"
        ]
        keyword_case = f"• {keywords[0] if keywords else '相关技术'} 在企业中的应用" if keywords else ""
        return "\n".join(cases[:3] + [keyword_case]) if keyword_case else "\n".join(cases)
    
    def _generate_summary(self, keywords: List[str]) -> str:
        """生成总结"""
        return f"总之，{keywords[0] if keywords else '这个技术'} 是一个值得学习和掌握的工具。它不仅能提高效率，还能为我们打开新的可能性。"


class ContentGenerator:
    """内容生成器"""
    
    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.posts: List[BlogPost] = []
        
    def generate_post(self, topic: str, tags: List[str] = None) -> BlogPost:
        """生成一篇博客文章"""
        title = self.provider.generate_title(topic)
        
        prompt = f"""
请为一篇关于「{topic}」的技术博客生成高质量内容。要求：
1. 至少 800 字
2. 结构清晰，有小标题
3. 包含实用的代码示例
4. 有深度的分析和见解
5. 用中文写作
6. 格式为 Markdown
"""
        content = self.provider.generate_content(prompt)
        
        post = BlogPost(
            title=title,
            content=content,
            tags=tags or ["技术", "自动化"],
            platform="medium"
        )
        
        self.posts.append(post)
        return post
    
    def generate_series(self, topics: List[str], base_tags: List[str] = None) -> List[BlogPost]:
        """生成系列文章"""
        posts = []
        for i, topic in enumerate(topics):
            tags = (base_tags or ["技术"]) + [f"系列{i+1}"]
            post = self.generate_post(topic, tags)
            posts.append(post)
        return posts
    
    def save_posts(self, filepath: str = "posts.json"):
        """保存文章到文件"""
        data = {
            "generated_at": datetime.datetime.now().isoformat(),
            "total_posts": len(self.posts),
            "posts": [post.to_dict() for post in self.posts]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath
    
    def export_markdown(self, output_dir: str = "posts"):
        """导出为 Markdown 文件"""
        os.makedirs(output_dir, exist_ok=True)
        for i, post in enumerate(self.posts):
            filename = f"{output_dir}/{i+1:03d}_{post.title[:30].replace(' ', '_')}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(post.content)
            post.status = "exported"
        return output_dir


class BlogPublisher:
    """博客发布器"""
    
    def __init__(self):
        self.medium_token = os.getenv("MEDIUM_TOKEN")
        self.wordpress_url = os.getenv("WORDPRESS_URL")
        self.wordpress_user = os.getenv("WORDPRESS_USER")
        self.wordpress_pass = os.getenv("WORDPRESS_PASS")
        
    def publish_to_medium(self, post: BlogPost) -> Dict:
        """发布到 Medium"""
        if not self.medium_token:
            return {"status": "skipped", "reason": "No MEDIUM_TOKEN"}
            
        url = "https://api.medium.com/v1/users/@me/posts"
        headers = {
            "Authorization": f"Bearer {self.medium_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "title": post.title,
            "contentFormat": "markdown",
            "content": post.content,
            "tags": post.tags[:5],  # Medium 最多5个标签
            "publishStatus": "draft"
        }
        
        # 这里实际会发送请求
        return {"status": "ready", "platform": "medium", "post": post.to_dict()}
    
    def publish_to_wordpress(self, post: BlogPost) -> Dict:
        """发布到 WordPress"""
        if not self.wordpress_url:
            return {"status": "skipped", "reason": "No WORDPRESS credentials"}
            
        # WordPress REST API
        url = f"{self.wordpress_url}/wp-json/wp/v2/posts"
        auth = (self.wordpress_user, self.wordpress_pass)
        data = {
            "title": post.title,
            "content": post.content,
            "status": "draft",
            "tags": post.tags
        }
        
        return {"status": "ready", "platform": "wordpress", "post": post.to_dict()}
    
    def publish_all(self, posts: List[BlogPost]) -> List[Dict]:
        """批量发布"""
        results = []
        for post in posts:
            result = self.publish_to_medium(post)
            results.append(result)
        return results


# 预设话题库
TOPIC_POOL = [
    "Python 自动化脚本编写",
    "AI 提示词工程技巧",
    "Docker 容器化部署教程",
    "Git 版本控制最佳实践",
    "Linux 服务器管理",
    "RESTful API 设计与实现",
    "数据库优化技巧",
    "Web 开发框架对比",
    "机器学习入门指南",
    "爬虫技术实战",
    "CI/CD 自动化部署",
    "云服务器配置",
    "正则表达式详解",
    "Python 并发编程",
    "API 自动化测试"
]


def main():
    """主函数 - 生成博客"""
    print("=" * 50)
    print("🚀 自动博客生成系统")
    print("=" * 50)
    
    # 选择 Provider
    print("\n📌 选择 AI Provider:")
    print("1. OpenAI (需要 API Key)")
    print("2. 免费模板生成")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1" and os.getenv("OPENAI_API_KEY"):
        provider = OpenAIProvider()
        print("✅ 使用 OpenAI 生成")
    else:
        provider = FreeProvider()
        print("✅ 使用免费模板生成")
    
    # 创建生成器
    generator = ContentGenerator(provider)
    
    # 生成话题数量
    n = input("\n📝 生成几篇文章 (默认3): ").strip()
    n = int(n) if n.isdigit() else 3
    
    # 随机选择话题
    import random
    topics = random.sample(TOPIC_POOL, min(n, len(TOPIC_POOL)))
    
    print(f"\n📌 将生成以下文章:")
    for i, topic in enumerate(topics, 1):
        print(f"   {i}. {topic}")
    
    # 生成文章
    print("\n⏳ 正在生成文章...")
    posts = generator.generate_series(topics)
    
    # 保存
    generator.save_posts("posts.json")
    generator.export_markdown("generated_posts")
    
    print(f"\n✅ 完成！生成了 {len(posts)} 篇文章")
    print("📁 已保存到:")
    print("   - posts.json")
    print("   - generated_posts/")
    
    # 显示第一篇预览
    if posts:
        print("\n📄 文章预览:")
        print("-" * 30)
        print(posts[0].title)
        print(f"字数: {posts[0].word_count} | 预计阅读: {posts[0].read_time} 分钟")
        print("-" * 30)


if __name__ == "__main__":
    main()
