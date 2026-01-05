# reference和reference-api目录中文化计划

## 项目概述
对reference和reference-api两个目录进行中文化，这两个目录包含Agno框架的参考文档和API文档。

## 文件统计
- reference目录: 148个.md文件
- reference-api目录: 3个文件（openapi.json, openapi.yaml, overview.mdx）+ schema子目录

## 中文化计划

### 第一阶段: reference目录中文化

1. reference/agent-os/目录
   - agent-os.mdx
   - authorization-config.mdx
   - client.mdx
   - configuration.mdx
   - jwt-middleware.mdx

2. reference/agents/目录
   - agent.mdx
   - metrics.mdx
   - remote-agent.mdx
   - run-response.mdx
   - session.mdx

3. reference/agno-infra/目录
   - cli/ws/config.mdx
   - cli/ws/create.mdx
   - cli/ws/delete.mdx
   - cli/ws/down.mdx
   - cli/ws/patch.mdx
   - cli/ws/restart.mdx
   - cli/ws/up.mdx

4. reference/compression/目录
   - compression-manager.mdx

5. reference/hooks/目录
   - base-guardrail.mdx
   - hook-decorator.mdx

6. reference/knowledge/目录
   - (待补充)

7. reference/memory/目录
   - (待补充)

8. reference/models/目录
   - aimlapi.mdx
   - anthropic.mdx
   - azure.mdx
   - azure-open-ai.mdx
   - bedrock.mdx
   - bedrock-claude.mdx
   - cohere.mdx
   - deepinfra.mdx
   - deepseek.mdx
   - fireworks.mdx
   - gemini.mdx
   - groq.mdx
   - huggingface.mdx
   - ibm-watsonx.mdx
   - internlm.mdx
   - langdb.mdx
   - meta.mdx
   - mistral.mdx
   - model.mdx
   - nebius.mdx
   - nvidia.mdx
   - ollama.mdx
   - ollama-tools.mdx
   - openai.mdx
   - openai-like.mdx
   - openrouter.mdx
   - perplexity.mdx
   - requesty.mdx
   - sambanova.mdx
   - together.mdx
   - vercel.mdx
   - xai.mdx

9. reference/reasoning/目录
   - (待补充)

10. reference/run/目录
    - (待补充)

11. reference/session/目录
    - (待补充)

12. reference/storage/目录
    - (待补充)

13. reference/teams/目录
    - (待补充)

14. reference/tools/目录
    - decorator.mdx
    - retry-agent-run.mdx
    - stop-agent-run.mdx
    - toolkit.mdx

15. reference/tracing/目录
    - (待补充)

16. reference/vector-db/目录
    - (待补充)

17. reference/workflows/目录
    - (待补充)

### 第二阶段: reference-api目录中文化

1. reference-api/overview.mdx

2. reference-api/schema/目录下的所有子目录和文件：
   - a2a/
   - agents/
   - agui/
   - core/
   - database/
   - evals/
   - health/
   - home/
   - knowledge/
   - memory/
   - metrics/
   - sessions/
   - slack/
   - teams/
   - traces/
   - whatsapp/
   - workflows/

3. openapi.json和openapi.yaml文件保持原样，因为它们是API规范文件，通常不需要翻译

## 实施步骤

1. 首先备份原始文件
2. 按目录逐一进行中文化
3. 每个文件翻译后检查格式是否正确
4. 翻译完成后进行整体检查

## 注意事项

- 代码示例和参数名称保持英文不变
- API端点、函数名、类名等技术术语保持英文
- 只翻译文档中的说明文字
- 保持Markdown格式不变