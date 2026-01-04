"""
自动化处理examples目录下所有mdx/md文件的中文化脚本
主要目标：
1. 翻译frontmatter中内容(title, description等)
2. 翻译正文中的说明文字
3. 翻译步骤标题(Step title)
4. 保持所有代码块、Python代码、终端命令不变
5. 保持所有的链接、路径、文件名不变
"""
import re
import os
from pathlib import Path


def extract_frontmatter(content):
    """提取并解析frontmatter"""
    pattern = r'^---\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        frontmatter_content = match.group(1)
        return match.group(0), content[match.end():]
    return None, content


def parse_frontmatter(frontmatter_text):
    """解析frontmatter文本为键值字典"""
    frontmatter = {}
    for line in frontmatter_text.strip().split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            frontmatter[key] = value
    return frontmatter


def translate_text(text):
    """翻译除代码块外的纯文本内容"""
    if not text.strip():
        return text

    # 更精确地识别代码块和组件标签，使用更复杂的正则表达式
    # 保护以下内容不被翻译：
    # 1. ```...``` 代码块
    # 2. `<Steps>...</Steps>` 组件标签
    # 3. `<Step ...>...</Step>` 组件标签
    # 4. `<Snippet ... />` 组件标签
    # 5. `<CodeGroup>...</CodeGroup>` 组件标签
    # 6. `<Link ...>...</Link>` 组件标签
    # 7. 单行代码 `...`

    # 按顺序保护各种块内容
    protected_items = []
    placeholder_pattern = "PLACEHOLDER_FOR_TRANSLATION_PROTECTION_{}"

    # 1. 保护 ```...``` 代码块 (多行) - 首先处理这个, 使用更精确的正则表达式
    code_block_pattern = r'```.*?```'
    def replace_code_block(match):
        idx = len(protected_items)
        placeholder = placeholder_pattern.format(idx)
        protected_items.append(match.group(0))  # 只保存内容
        return placeholder

    text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)

    # 2. 保护 `...` 行内代码
    inline_code_pattern = r'`[^`]*`'
    def replace_inline_code(match):
        idx = len(protected_items)
        placeholder = placeholder_pattern.format(idx)
        protected_items.append(match.group(0))
        return placeholder

    text = re.sub(inline_code_pattern, replace_inline_code, text)

    # 3. 保护 MDX 组件 - 使用更精确的正则表达式
    # 先处理自闭合标签
    self_closing_pattern = r'<(Snippet|Step)[^>]*/>'
    def replace_self_closing(match):
        idx = len(protected_items)
        placeholder = placeholder_pattern.format(idx)
        protected_items.append(match.group(0))
        return placeholder

    text = re.sub(self_closing_pattern, replace_self_closing, text)

    # 处理带内容的标签
    component_pattern = r'<(Steps|Step|CodeGroup|Link)[^>]*>.*?</\1>'
    def replace_component(match):
        idx = len(protected_items)
        placeholder = placeholder_pattern.format(idx)
        protected_items.append(match.group(0))
        return placeholder

    text = re.sub(component_pattern, replace_component, text, flags=re.DOTALL)

    # 4. 保护单独的开始/结束标签
    single_tag_pattern = r'<(Steps|Step|Snippet|CodeGroup|Link)[^>]*>|</(Steps|Step|Snippet|CodeGroup|Link)>'
    def replace_single_tag(match):
        idx = len(protected_items)
        placeholder = placeholder_pattern.format(idx)
        protected_items.append(match.group(0))
        return placeholder

    text = re.sub(single_tag_pattern, replace_single_tag, text)

    # 现在对未被保护的文本进行翻译
    # 首先处理Step title="..."中的文本
    def translate_step_title(match):
        full_match = match.group(0)
        title_content = match.group(1)
        # 只翻译标题中的英文文本
        translated_title_content = title_content.strip()
        # 英文到中文的翻译映射
        translations = {
            "Install libraries": "安装库",
            "Set your API key": "设置API密钥",
            "Run Agent": "运行代理",
            "Run Team": "运行团队",
            "Run Workflow": "运行工作流",
            "Create Python file": "创建Python文件",
            "Run the script": "运行脚本",
            "Add environment variables": "添加环境变量",
            "Set up environment": "设置环境",
            "Run Python file": "运行Python文件",
            "Export your OpenAI API key": "导出您的OpenAI API密钥",
            "Create Python File": "创建Python文件",
            "Find all example code": "查找所有示例代码",
            "Set up API key": "设置API密钥",
            "Set up API keys": "设置API密钥",
            "Setup": "设置",
            "Use": "使用",
            "Usage": "用法",
            "Set your API keys": "设置您的API密钥",
            "Create virtual environment": "创建虚拟环境",
            "Set up virtual environment": "设置虚拟环境",
            "Install dependencies": "安装依赖项",
            "Get API key": "获取API密钥",
            "Add API key": "添加API密钥",
            "Run application": "运行应用程序",
            "Test the application": "测试应用程序",
            "Configure settings": "配置设置",
            "Initialize project": "初始化项目",
            "Build project": "构建项目",
            "Deploy application": "部署应用程序",
            "Start server": "启动服务器",
            "View in browser": "在浏览器中查看",
            "Set up database": "设置数据库",
            "Import data": "导入数据",
            "Export data": "导出数据",
            "Run tests": "运行测试",
            "Create account": "创建账户",
            "Login to account": "登录账户",
            "Configure authentication": "配置认证",
            "Set permissions": "设置权限",
            "Create workspace": "创建工作区",
            "Add members": "添加成员",
            "Configure team": "配置团队",
            "Install tool": "安装工具",
            "Configure tool": "配置工具",
            "Run tool": "运行工具",
            "Create model": "创建模型",
            "Configure model": "配置模型",
            "Train model": "训练模型",
            "Test model": "测试模型",
            "Deploy model": "部署模型",
            "Monitor model": "监控模型",
            "Update model": "更新模型",
            "Create workflow": "创建工作流",
            "Configure workflow": "配置工作流",
            "Execute workflow": "执行工作流",
            "Manage workflow": "管理工作流",
            "Create agent": "创建代理",
            "Configure agent": "配置代理",
            "Run agent": "运行代理",
            "Manage agent": "管理代理",
            "Create team": "创建团队",
            "Configure team": "配置团队",
            "Run team": "运行团队",
            "Manage team": "管理团队",
            "Set API key": "设置API密钥",
            "Set API keys": "设置API密钥",
            "Create database": "创建数据库",
            "Connect to database": "连接到数据库",
            "Query database": "查询数据库",
            "Update database": "更新数据库",
            "Backup database": "备份数据库",
            "Restore database": "恢复数据库",
            "Create vector database": "创建向量数据库",
            "Connect to vector database": "连接到向量数据库",
            "Query vector database": "查询向量数据库",
            "Configure vector database": "配置向量数据库",
            "Create knowledge base": "创建知识库",
            "Add knowledge": "添加知识",
            "Query knowledge": "查询知识",
            "Update knowledge": "更新知识",
            "Create storage": "创建存储",
            "Configure storage": "配置存储",
            "Use storage": "使用存储",
            "Create memory": "创建内存",
            "Use memory": "使用内存",
            "Configure memory": "配置内存",
            "Create session": "创建会话",
            "Use session": "使用会话",
            "Configure session": "配置会话",
            "Create cache": "创建缓存",
            "Use cache": "使用缓存",
            "Configure cache": "配置缓存",
            "Create search": "创建搜索",
            "Use search": "使用搜索",
            "Configure search": "配置搜索",
            "Create tool": "创建工具",
            "Use tool": "使用工具",
            "Configure tool": "配置工具",
            "Create function": "创建函数",
            "Use function": "使用函数",
            "Configure function": "配置函数",
            "Create class": "创建类",
            "Use class": "使用类",
            "Configure class": "配置类",
            "Create module": "创建模块",
            "Use module": "使用模块",
            "Configure module": "配置模块",
            "Create plugin": "创建插件",
            "Use plugin": "使用插件",
            "Configure plugin": "配置插件",
            "Create library": "创建库",
            "Use library": "使用库",
            "Configure library": "配置库",
        }
        for eng, chn in translations.items():
            translated_title_content = translated_title_content.replace(eng, chn)

        return f'title="{translated_title_content}"'

    # 对Step title="..."进行翻译
    text = re.sub(r'title="([^"]*)"', translate_step_title, text)

    # 对普通文本进行翻译
    text_translations = {
        "Install libraries": "安装库",
        "Set your API key": "设置API密钥",
        "Run Agent": "运行代理",
        "Run Team": "运行团队",
        "Run Workflow": "运行工作流",
        "Usage": "用法",
        "Code": "代码",
        "Use": "使用",
        "Set up": "设置",
        "Setup": "设置",
        "API key": "API密钥",
        "virtual environment": "虚拟环境",
        "dependencies": "依赖项",
        "application": "应用程序",
        "environment": "环境",
        "configuration": "配置",
        "settings": "设置",
        "authentication": "认证",
        "permissions": "权限",
        "workspace": "工作区",
        "members": "成员",
        "tool": "工具",
        "model": "模型",
        "workflow": "工作流",
        "agent": "代理",
        "team": "团队",
        "database": "数据库",
        "vector database": "向量数据库",
        "knowledge base": "知识库",
        "storage": "存储",
        "memory": "内存",
        "session": "会话",
        "cache": "缓存",
        "search": "搜索",
        "function": "函数",
        "class": "类",
        "module": "模块",
        "plugin": "插件",
        "library": "库",
        "This example shows": "此示例展示",
        "This example demonstrates": "此示例演示",
        "shows how to": "展示如何",
        "demonstrates how to": "演示如何",
        "demonstrates how": "演示如何",
        "demonstrates the": "演示",
        "demonstrates": "演示",
        "shows the": "展示",
        "shows": "展示",
        "to create": "创建",
        "to use": "使用",
        "to configure": "配置",
        "to set up": "设置",
        "to install": "安装",
        "to run": "运行",
        "to manage": "管理",
        "to build": "构建",
        "to deploy": "部署",
        "to test": "测试",
        "to monitor": "监控",
        "to update": "更新",
        "explains how to": "解释如何",
        "explains how": "解释如何",
        "explains": "解释",
        "Learn how to": "学习如何",
        "Learn how": "学习如何",
        "Learn": "学习",
        "understand how to": "理解如何",
        "understand how": "理解如何",
        "understand": "理解",
        "Explore": "探索",
        "Explore how to": "探索如何",
        "Explore how": "探索如何",
        "Discover": "发现",
        "Discover how to": "发现如何",
        "Discover how": "发现如何",
        "Find out": "了解",
        "Find out how to": "了解如何",
        "Find out how": "了解如何",
        "Get started": "开始",
        "Getting started": "入门",
        "Introduction": "介绍",
        "Overview": "概述",
        "Introduction to": "介绍",
        "Introduction on": "关于的介绍",
        "Basic": "基础",
        "Advanced": "高级",
        "Simple": "简单",
        "Complex": "复杂",
        "Example": "示例",
        "Tutorial": "教程",
        "Guide": "指南",
        "Step by step": "逐步",
        "instructions": "说明",
        "instruction": "说明",
        "commands": "命令",
        "command": "命令",
        "script": "脚本",
        "scripts": "脚本",
        "file": "文件",
        "files": "文件",
        "Python": "Python",  # 保持技术术语不变
        "OpenAI": "OpenAI",  # 保持技术术语不变
        "API": "API",  # 保持技术术语不变
        "Key": "密钥",
        "Keys": "密钥",
        "export": "导出",
        "Export": "导出",
        "environment variable": "环境变量",
        "environment variables": "环境变量",
        "bash": "bash",  # 保持命令不变
        "python": "python",  # 保持命令不变
        "pip": "pip",  # 保持命令不变
        "touch": "touch",  # 保持命令不变
        "GitHub": "GitHub",  # 保持专有名词不变
        "Mac": "Mac",  # 保持操作系统名称不变
        "Windows": "Windows",  # 保持操作系统名称不变
        "Linux": "Linux",  # 保持操作系统名称不变
        "click": "点击",
        "link": "链接",
        "links": "链接",
        "view": "查看",
        "see": "查看",
        "available": "可用的",
        "available code": "可用代码",
        "all": "所有",
        "all available": "所有可用",
        "all available code": "所有可用代码",
        "repository": "存储库",
        "code repository": "代码存储库",
        "Cookbook": "Cookbook",
        "cookbook": "cookbook",
        "examples": "示例",
        "example": "示例",
        "available examples": "可用示例",
        "all examples": "所有示例",
        "Find all": "查找所有",
        "find all": "查找所有",
        "all available examples": "所有可用示例",
        "Explore all": "探索所有",
        "explore all": "探索所有",
        "more information": "更多信息",
        "more info": "更多信息",
        "additional information": "附加信息",
        "further information": "进一步信息",
        "details": "详细信息",
        "detail": "详细信息",
        "information": "信息",
        "info": "信息",
        "about": "关于",
        "related to": "关于",
        "related": "相关",
        "associated with": "与...相关",
        "connected to": "与...连接",
    }

    # 应用文本翻译
    for eng, chn in text_translations.items():
        text = text.replace(eng, chn)

    # 恢复受保护的组件 - 按相反顺序进行，以避免占位符被再次替换
    for i in range(len(protected_items) - 1, -1, -1):
        placeholder = placeholder_pattern.format(i)
        text = text.replace(placeholder, protected_items[i])

    return text


def update_frontmatter(frontmatter_data):
    """翻译frontmatter内容"""
    updated_frontmatter = {}
    translations = {
        "title": "标题",
        "description": "描述",
        "CSV Tools": "CSV工具",
        "SQL Tools": "SQL工具",
        "DuckDB Tools": "DuckDB工具",
    }

    for key, value in frontmatter_data.items():
        # 翻译frontmatter中的某些键值内容，但不是键本身
        translated_value = value
        for eng, chn in translations.items():
            translated_value = translated_value.replace(eng, chn)

        updated_frontmatter[key] = translated_value

    return updated_frontmatter


def translate_file(file_path):
    """翻译单个文件的内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取frontmatter
    frontmatter_str, remaining_content = extract_frontmatter(content)

    if frontmatter_str:
        # 解析并翻译frontmatter
        frontmatter_part = frontmatter_str[4:-3].strip()  # 移除开头的---和结尾的---
        frontmatter_data = parse_frontmatter(frontmatter_part)

        # 翻译frontmatter数据
        updated_frontmatter_data = update_frontmatter(frontmatter_data)

        # 重构frontmatter
        new_frontmatter_lines = ['---']
        for key, value in updated_frontmatter_data.items():
            new_frontmatter_lines.append(f'{key}: {value}')
        new_frontmatter_lines.append('---\n')
        new_frontmatter = '\n'.join(new_frontmatter_lines)

        # 翻译剩余内容（非frontmatter部分）
        translated_remaining_content = translate_text(remaining_content)

        # 组合新内容
        new_content = new_frontmatter + translated_remaining_content
    else:
        # 没有frontmatter，则翻译全部内容
        new_content = translate_text(content)

    # 写回翻译后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    print("开始对 examples 目录中的所有 mdx/md 文件进行中文化...")

    file_list_path = './file_list.txt'  # 包含所有文件列表的路径

    with open(file_list_path, 'r', encoding='utf-8') as f:
        file_paths = [line.strip() for line in f.readlines() if line.strip()]

    print(f"待翻译文件总计：{len(file_paths)} 个")

    failed_files = []
    for i, file_path in enumerate(file_paths, 1):
        print(f"[{i}/{len(file_paths)}] 正在处理: {file_path}")
        try:
            translate_file(file_path)
            print(f"  ✓ 翻译完成")
        except Exception as e:
            print(f"  ✗ 处理失败: {str(e)}")
            failed_files.append(file_path)

    print("\n" + "="*50)
    print(f"翻译任务完成！成功: {len(file_paths)-len(failed_files)}, 失败: {len(failed_files)}")
    if failed_files:
        print("失败的文件:")
        for f in failed_files:
            print(f"  - {f}")


if __name__ == "__main__":
    main()