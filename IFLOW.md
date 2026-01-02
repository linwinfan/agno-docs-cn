# Agno 中文文档项目

## 项目概述

Agno 是一个用于构建、运行和管理多智能体系统的统一框架。该项目是 Agno 的中文文档站点，提供完整的中文技术文档，帮助中文用户理解和使用 Agno 框架。

### 核心功能

- **智能体**: 创建具有记忆、知识、工具和推理能力的 AI 智能体
- **团队**: 多个智能体协同工作完成复杂任务
- **工作流**: 定义和执行多步骤任务的强大方式
- **AgentOS**: 生产就绪的运行时环境，完全在用户自己的基础设施内运行

### 项目类型

这是一个基于 Mintlify 的文档站点项目，使用 MDX 格式编写文档内容。

## 项目结构

```
agno-docs-cn/
├── agent-os/           # AgentOS 相关文档
├── basics/             # 基础概念文档
│   ├── agents/         # 智能体相关文档
│   ├── teams/          # 团队相关文档
│   ├── workflows/      # 工作流相关文档
│   └── ...
├── deploy/             # 部署相关文档
├── examples/           # 示例文档
├── faq/                # 常见问题
├── get-started/        # 入门指南
├── how-to/             # 操作指南
├── images/             # 图片资源
├── integrations/       # 集成文档
├── reference/          # 参考文档
├── reference-api/      # API 参考
├── templates/          # 模板
├── tutorials/          # 教程
├── videos/             # 视频资源
├── index.mdx           # 首页
├── introduction.mdx    # 介绍页
├── docs.json           # Mintlify 配置文件
└── README.md           # 项目说明
```

## 构建和运行

### 环境要求

- Node.js
- npm

### 安装依赖

```bash
# 安装 Mintlify CLI
npm i -g mint

# 安装项目依赖
npm install
```

### 本地开发

```bash
# 启动开发服务器
mint dev
```

### 构建生产版本

```bash
# 构建静态文件
mint build
```

### API 文档生成

该项目支持从本地运行的 AgentOS 实例生成 API 文档：

```bash
# 从本地 AgentOS 获取 OpenAPI 规范
curl -o reference-api/openapi.json http://localhost:7777/openapi.json

# 使用 swagger-cli 转换为 yaml 格式
swagger-cli bundle reference-api/openapi.json --outfile reference-api/openapi.yaml --type yaml

# 生成类型化 API 文档
px @mintlify/scraping@latest openapi-file reference-api/openapi.json -o reference-api/schema
```

## 开发约定

### 文档规范

- 所有文档使用 `.mdx` 格式
- 文档应包含适当的 frontmatter 元数据
- 使用中文编写，保持术语一致性
- 代码示例应简洁明了，包含必要的注释

### 内容组织

- **概述**: 提供功能的高层次介绍
- **指南**: 分步骤的操作说明
- **参考**: 详细的 API 和配置参考
- **示例**: 实际使用场景的代码示例

### 贡献流程

1. 创建 issue 描述建议或问题
2. Fork 项目仓库
3. 创建功能分支
4. 提交更改
5. 创建 Pull Request

### 术语翻译

保持以下术语的一致翻译：
- Agent → 智能体
- Team → 团队
- Workflow → 工作流
- Tool → 工具
- Model → 模型
- API → API
- Framework → 框架
- Runtime → 运行时

## 文档导航

文档按以下结构组织：

1. **首页**: 项目概述和快速导航
2. **入门指南**: 基础概念和快速开始
3. **基础概念**: 详细介绍各个核心概念
4. **AgentOS**: 生产运行时环境文档
5. **参考文档**: 开发者完整的 SDK 和 API 参考
6. **帮助**: 常见问题和支持资源

## 技术栈

- **文档框架**: Mintlify
- **内容格式**: MDX
- **样式**: 自定义 CSS 与 Mintlify 主题
- **构建工具**: Mintlify CLI
- **版本控制**: Git

## 注意事项

- 文档中的代码示例应保持最新，与实际 API 保持一致
- 图片资源应优化大小，确保加载性能
- 外部链接应定期检查，确保有效性
- 文档应保持与英文版本的同步更新

## 联系方式

- **Discord**: [社区讨论](https://agno.link/discord)
- **GitHub**: [提交 issue](https://github.com/agno-agi/agno-docs-cn)
- **Email**: [联系支持](mailto:docs@agno.com)