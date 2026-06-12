# Palest Ink

> 好记性不如烂笔头。  
> The palest ink is better than the strongest memory.

[English](./README.md)

面向 AI Agent 的无记忆文档架构。以用户自行声明的显式项目文档取代隐式自动积累的记忆系统，文档按四层分类管理。

## 为什么

隐式记忆系统——Mem0、MemPalace、自动总结型 MEMORY 文件、向量数据库记忆插件——都有这些致命缺陷：

- **无法控制的积累。** 自动总结系统会自行整理和改写记忆，你无法确定里面有什么、是否还有存在的必要。
- **存储不透明。** 记忆存在向量数据库或压缩摘要里，无法直接阅读、编辑或验证。
- **大小限制导致有损压缩。** 记忆系统有 token 或存储上限，满了之后旧信息会被静默丢弃或合并——你不知道丢了什么。
- **仅对 Agent 有价值。** 记忆的组织方式是给 Agent 用的，对协作者没有帮助，不支持新人接手，无法随工具迁移。

文档解决所有这些问题。文档可检查、可编辑、可删除、可版本控制，对人和 Agent 都有用。

## 原则

**显式优于隐式。** 所有知识都在你声明的文件里，路径明确，没有隐藏状态。

**用户控制映射。** Agent 按你的 INK.md 行动，不自行决定文件归属。修改映射需要你批准。

**渐进加载。** Agent 只读取当前任务需要的文档，不做全量加载。

**新鲜优于完整。** 过时信息不如没有。保持文档更新，或删除。

## 四层级分类

| 层级 | 核心问题 | 典型内容 |
|------|------|----------|
| Conceptual | 为什么 | 愿景、设计决策、约束、反目标、领域模型 |
| Structural | 在哪里 | 文件布局、模块关系、数据模型、内容组织 |
| Behavioral | 怎么做 | 规范、流程、规则、风格指南、检查清单 |
| Operational | 发生了什么 | 会话记录、变更日志、任务记录、调试笔记 |

这套分类是通用的，适用于软件项目、小说手稿、研究工作、产品规划——任何有目标、有结构、有流程、有历史的项目。

## 使用方法

```bash
npx skills@latest add kenpusney/palest-ink
```

1. 将 `skills/palest-ink/assets/INK.md` 复制到项目根目录（或 `.agents/INK.md`）。
2. 在四个层级下填入文件和目录路径。
3. Agent 启动时读取 INK.md，按需加载相关文档。
4. Agent 将发现写入对应层级，有 operational 内容时写入 operational 路径。
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
| 不透明（向量数据库、压缩摘要） | 开放的纯文本文件，随时可读 |
| 自动积累，难以控制 | 用户管理，可清理 |
| 大小限制导致有损压缩 | 没有大小限制，按需增长 |
| 仅对 Agent 有价值 | 对人和 Agent 都有价值 |
| 绑定工具/平台 | 可移植、纯文本 |

## 局限

- **冷启动成本。** 新项目没有文档，首次启用需要搭建 INK.md 和初始文档。
- **需要自律。** Agent 负责写入，人负责清理。长期忽视的文档会变成这套架构本想解决的冗余问题。
- **不是知识库。** Palest Ink 管理项目内部知识，不替代 Wiki、Notion 或面向外部读者的长文文档。
- **Agent 判断有差异。** 分类归属取决于 Agent 对项目的理解，INK.md 的映射应定期检查。

## 建议

- 从小处开始。映射已有的文件。不要为了填满层级而创建文档。
- 每月检查 operational 日志。归档或删除超过 30 天且无持续价值的内容。
- 将 INK.md 视作活文档。项目结构变化时同步更新。
- 团队项目中将 INK.md 和引用的文档纳入版本控制。
