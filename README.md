# Antu58 My Skills

面向 ChatGPT 与 Codex 的个人工作流插件，包含两个可复用 skill：

- `okf-project-docs`：创建、重构和更新中文优先的 OKF 项目文档，并生成支持 Mermaid 图表拖拽缩放的单文件 `viewer.html`。
- `model-raw-requirements`：将零散、非正式或互相冲突的需求材料整理为可评审的 OKF 业务模型。

## 安装

首次注册 Git marketplace：

```bash
codex plugin marketplace add antu58/myskills
```

安装插件：

```bash
codex plugin add myskills@antu58-myskills
```

安装后请创建一个新任务，让 Codex 加载插件中的 skill。

## 使用

```text
$okf-project-docs 为当前项目创建 OKF 文档。
$model-raw-requirements 将这些需求材料整理为业务模型。
```

也可以直接描述任务，由 Codex 根据 skill 的 `description` 自动选择工作流。

## 更新

维护者更新 skill 后，修改 `plugins/myskills/.codex-plugin/plugin.json` 中的版本号，提交并推送 Git。

使用者刷新 marketplace 并重新安装插件：

```bash
codex plugin marketplace upgrade antu58-myskills
codex plugin add myskills@antu58-myskills
```

然后创建一个新任务测试更新后的版本。

## 仓库结构

```text
.agents/plugins/marketplace.json
plugins/myskills/.codex-plugin/plugin.json
plugins/myskills/skills/okf-project-docs/
plugins/myskills/skills/model-raw-requirements/
```

## License

MIT。第三方组件说明见 `THIRD_PARTY_NOTICES.md`。
