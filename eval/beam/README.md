# BEAM × Palest Ink Evaluation

使用 BEAM benchmark 的数据验证 Palest Ink 文档架构的效果。

## 方法

beam_eval.py 通过 OpenAI 兼容 API 调用模型，给模型真实的工具调用能力（Read/Write/Edit/Glob/Grep），让它按 Palest Ink 框架处理对话。

### 提取阶段 (extract)

1. 预建 INK.md + 11 个文档模板
2. 按轮次依次 feed 对话，每 5 轮一组
3. 模型用工具读取已有文档、编辑追加新信息
4. 最后生成 summary

### 回答阶段 (answer)

1. 给模型 SKILL.md + INK.md 路径
2. 逐题提问，模型自行搜索相关文档
3. 记录每个问题读取了哪些文件

## 使用

```bash
# 设置 .env
BASE_URL=https://...
API_TOKEN=...
MODEL=mimo-v2.5-pro

# 提取
python eval/beam/beam_eval.py extract 1 2 3 4 5

# 回答
python eval/beam/beam_eval.py answer 1 2 3 4 5
```

## 100K 结果

事实类问题（extraction、instruction、preference）得分 92-100%。
推理类问题（contradiction、event_ordering、multi_session）得分 20-38%。
符合 Palest Ink 的设计取舍：用对话保真度换取项目知识的清晰度。
