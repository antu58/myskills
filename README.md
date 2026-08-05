# Antu58 My Skills

面向 ChatGPT 与 Codex 的个人 Skill Marketplace。每个 Skill 使用独立 Plugin 打包，可以按需安装；后续新增的 Skill 也会继续发布到这个仓库。

## 可用 Plugin

| Plugin | 用途 |
| --- | --- |
| `okf-project-docs` | 创建、重构和更新中文优先的 OKF 项目文档，并生成支持 Mermaid 图表拖拽缩放的单文件 `viewer.html`。 |
| `model-raw-requirements` | 将零散、非正式或互相冲突的需求材料整理为可评审的 OKF 业务模型。 |

## 安装

每台机器首次使用时注册 Git Marketplace：

```bash
codex plugin marketplace add antu58/myskills
```

按需安装一个或两个 Plugin：

```bash
codex plugin add okf-project-docs@antu58-myskills
codex plugin add model-raw-requirements@antu58-myskills
```

安装后请创建一个新任务，让 Codex 加载 Plugin 中的 Skill。

## 从旧版 `myskills` Plugin 迁移

旧版曾将两个 Skill 打包在一个 `myskills` Plugin 中。先刷新 Marketplace 并移除旧 Plugin，再按需安装新的独立 Plugin：

```bash
codex plugin marketplace upgrade antu58-myskills
codex plugin remove myskills@antu58-myskills
codex plugin add okf-project-docs@antu58-myskills
codex plugin add model-raw-requirements@antu58-myskills
```

## 使用

```text
$okf-project-docs 为当前项目创建 OKF 文档。
$model-raw-requirements 将这些需求材料整理为业务模型。
```

也可以直接描述任务，由 Codex 根据 Skill 的 `description` 自动选择工作流。

## 更新现有 Skill

维护者修改对应 Plugin 下的 Skill，并提升该 Plugin 的 `.codex-plugin/plugin.json` 版本，然后提交并推送 Git。

使用者刷新 Marketplace 并重新安装需要更新的 Plugin：

```bash
codex plugin marketplace upgrade antu58-myskills
codex plugin add <plugin-name>@antu58-myskills
```

随后创建一个新任务测试新版本。

## 添加新 Skill

新增 Skill 时，为它创建同名的独立 Plugin，并在 `.agents/plugins/marketplace.json` 中增加一个条目：

```text
plugins/<plugin-name>/.codex-plugin/plugin.json
plugins/<plugin-name>/skills/<skill-name>/SKILL.md
```

这样仓库保持一个 Marketplace，所有 Skill 又能独立安装和更新。

## 仓库结构

```text
.agents/plugins/marketplace.json
plugins/okf-project-docs/.codex-plugin/plugin.json
plugins/okf-project-docs/skills/okf-project-docs/
plugins/model-raw-requirements/.codex-plugin/plugin.json
plugins/model-raw-requirements/skills/model-raw-requirements/
```

## License

MIT。第三方组件说明见 `THIRD_PARTY_NOTICES.md`。
