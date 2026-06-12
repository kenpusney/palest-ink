# Palest Ink — Eval Results

## Iteration 1

3 个场景，7 条 assertions，全部通过。

### Eval 1: 首次引导

**Prompt**: 帮我用 Palest Ink 整理一下这个项目的文档

**Project**: 简单的 Next.js 看板项目，无 INK.md

**Assertions** (3/3 ✅):
- INK.md 被创建在项目根目录
- INK.md 包含四个层级 section
- 映射包含项目现有文件（README.md, package.json, src/index.ts）

**Observations**: Agent 把 README.md 同时归到 Conceptual 和 Behavioral，因为里面既有项目概述也有开发约定。给 Operational 层加了"暂无操作日志"占位。分类判断合理。

| Metric | Value |
|--------|-------|
| Duration | 132s |
| Tokens | 18,451 |

### Eval 2: 按需加载

**Prompt**: 这个项目的 API 认证是怎么实现的？

**Project**: 已有 INK.md + 四层文档

**Assertions** (2/2 ✅):
- 回答包含 JWT + Refresh Token 双令牌机制
- 基于 architecture.md 内容回答（15分钟、7天、HttpOnly Cookie）

**Observations**: Agent 明确列出"intentionally did NOT load"的文档（changelog）并解释原因。只加载了 Conceptual 和 Behavioral 层。渐进加载行为正确。

| Metric | Value |
|--------|-------|
| Duration | 160s |
| Tokens | 19,383 |

### Eval 3: 写回分类

**Prompt**: 记一下数据库连接池泄漏问题

**Project**: 已有 INK.md + operational 文档

**Assertions** (2/2 ✅):
- 调试记录写入 docs/operational/debug-notes.md（含连接池、release()）
- INK.md 未被修改（SHA256 哈希一致）

**Observations**: 正确分类到 Operational（"发生了什么"），写入对应路径，未动 INK.md。

| Metric | Value |
|--------|-------|
| Duration | 72s |
| Tokens | 16,718 |

## Summary

| Eval | Assertions | Duration | Tokens |
|------|-----------|----------|--------|
| Bootstrapping | 3/3 ✅ | 132s | 18.5k |
| Selective load | 2/2 ✅ | 160s | 19.4k |
| Write-back | 2/2 ✅ | 72s | 16.7k |
| **Total** | **7/7** | **364s** | **54.5k** |

Skill 验证通过，核心行为（引导、按需加载、写回分类、INK.md 保护）均符合预期。
