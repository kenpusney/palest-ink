# Palest Ink

> 好记性不如烂笔头。  
> The palest ink is better than the best memory.

[English](./README.md)

面向 AI Agent 的无记忆文档架构。用显式的、由用户声明的项目文档替代隐式自动积累的记忆系统，文档按四层级归类。

## 为什么

Agent 记忆系统——每日日志、MEMORY.md、云端画像、对话搜索——共享同一套致命缺陷：

- **无声漂移。** 信息在没有任何警告的情况下过时。你无法知道 Agent 还相信什么、哪些已经失效。
- **上下文污染。** 每次会话加载全部累积记忆，无论是否相关，浪费上下文窗口，稀释聚焦能力。
- **不可检查。** 记忆是隐藏状态。你无法打开文件查看 Agent 记得什么、验证是否正确、删除错误内容。
- **仅对 Agent 有价值。** 记忆文件只服务 Agent。对协作者无用，不支持新人上手，无法随工具迁移。

文档解决所有这些问题。文档可检查、可编辑、可删除、可版本控制，对人和 Agent 都有用。

## 原则

**显式优于隐式。** 每一条知识都存在于你声明的命名文件、已知路径中。没有隐藏。

**用户拥有地图。** Agent 遵循你的 INK.md——它不决定文件放在哪里。任何映射变更需你许可。

**渐进加载。** Agent 只读取当前任务需要的文档，不倾倒它曾经知道的一切。

**新鲜优于完整。** 过时信息不如没有。保持文档更新，或删除。

## 四层级分类

| 层级 | 问题 | 典型内容 |
|------|------|----------|
| Conceptual | 为什么 | 愿景、设计决策、约束、反目标、领域模型 |
| Structural | 在哪里 | 文件布局、模块关系、数据模型、内容组织 |
| Behavioral | 怎么做 | 规范、流程、规则、风格指南、检查清单 |
| Operational | 发生了什么 | 会话记录、变更日志、任务记录、调试笔记 |

分类法是通用的。同样适用于软件项目、小说手稿、研究工作、产品规划——任何有目标、有结构、有流程、有历史的项目。

## 使用方法

```bash
npx skills@latest add kenpusney/palest-ink
```

1. 将 `assets/INK.md` 复制到项目根目录（或 `.agents/INK.md`）。
2. 在四个层级下填入文件和目录路径。
3. Agent 在会话开始时读取 INK.md，按路径加载。
4. Agent 将发现写入对应层级，会话结束时将摘要写入 operational 路径。
5. 你可随时修改 INK.md。Agent 未经许可不得修改。

### INK.md 示例

```markdown
# INK.md

## Conceptual
- docs/conceptual/design-principles.md
- docs/conceptual/adr/
- docs/conceptual/domain-reference.md

## Structural
- docs/structural/architecture.md
- docs/structural/module-map.md
- docs/structural/data-models.md

## Behavioral
- docs/behavioral/coding-standards.md
- docs/behavioral/project-rules.md
- docs/behavioral/api-contracts.md

## Operational
- docs/operational/changelog.md
- docs/operational/sessions/
- docs/operational/debugging-notes.md
```

也可以指向单个文件而非目录，或两者混用。没有预设布局——INK.md 反映的是你的项目，不是模板。

## 相对自动记忆系统的优势

| 自动记忆 | Palest Ink |
|---|---|
| 隐藏、不可检查的状态 | 开放、可读的文件 |
| 无限制累积 | 可策划、可修剪 |
| 仅对 Agent 有价值 | 对人 + Agent 都有价值 |
| 上下文窗口膨胀 | 按需渐进加载 |
| 无声漂移 | 显式维护 |
| 绑定工具/平台 | 可移植、纯文本 |

## 局限

- **冷启动成本。** 新项目没有文档。首次启用需要 bootstrapping INK.md 和初始文档。
- **需要自律。** Agent 写入文档，但人负责修剪。被忽视的文档会成为这套架构试图消灭的冗余本身。
- **不是知识库。** Palest Ink 组织项目知识——它不替代 Wiki、Notion 或面向外部读者的长文文档。
- **Agent 判断有差异。** 分类归属依赖 Agent 的理解。定期检查 INK.md 的映射。

## 建议

- 从小处开始。映射已有的文件。不要为了填满层级而创建文档。
- 每月检查 operational 日志。归档或删除超过 30 天且无持续价值的内容。
- 将 INK.md 视作活文档。项目结构变化时同步更新。
- 团队项目中将 INK.md 和引用的文档纳入版本控制。
