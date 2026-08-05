# Antu58 My Skills

这是一个公开的 ChatGPT 与 Codex Skill Marketplace：[github.com/antu58/myskills](https://github.com/antu58/myskills)。

仓库中的每个 Skill 都使用同名的独立 Plugin 打包，可以按需安装、更新和卸载。后续新增的 Skill 也会继续发布到这个 Marketplace，不需要为每个 Skill 单独注册仓库。

## Skill 列表

| Plugin / Skill | 作用 | 典型用途 |
| --- | --- | --- |
| `okf-project-docs` | 创建、重构和维护中文优先的 OKF 项目文档，并生成单文件 `viewer.html`。Viewer 使用真实相对路径和原始文件名，支持 Mermaid 流程图、时序图的拖拽、缩放和全屏查看。 | 架构文档、服务/API/数据/事件文档、Runbook、ADR、项目知识库。 |
| `model-raw-requirements` | 将零散、非正式或互相冲突的需求材料整理为可评审、可追溯的 OKF 业务模型。 | 从文档、表格、会议记录、聊天和利益相关者陈述中提炼范围、角色、流程、时序和状态模型。 |

## 首次安装

### 1. 注册 Marketplace

每台机器只需执行一次：

```bash
codex plugin marketplace add antu58/myskills
```

注册后的 Marketplace 名称是 `antu58-myskills`。

### 2. 按需安装 Skill

只安装 OKF 项目文档 Skill：

```bash
codex plugin add okf-project-docs@antu58-myskills
```

只安装原始需求建模 Skill：

```bash
codex plugin add model-raw-requirements@antu58-myskills
```

需要两个 Skill 时可以都执行：

```bash
codex plugin add okf-project-docs@antu58-myskills
codex plugin add model-raw-requirements@antu58-myskills
```

安装完成后请创建一个新的 Codex 任务，让 Codex 加载新安装的 Skill。

### 3. 检查安装状态

```bash
codex plugin marketplace list
codex plugin list --marketplace antu58-myskills
```

## 更新

已经安装过 Plugin 后，更新时仍然使用相同的 `codex plugin add` 命令，但需要先刷新 Git Marketplace。

更新 `okf-project-docs`：

```bash
codex plugin marketplace upgrade antu58-myskills
codex plugin add okf-project-docs@antu58-myskills
```

更新 `model-raw-requirements`：

```bash
codex plugin marketplace upgrade antu58-myskills
codex plugin add model-raw-requirements@antu58-myskills
```

同时更新两个 Plugin 时，Marketplace 只需刷新一次：

```bash
codex plugin marketplace upgrade antu58-myskills
codex plugin add okf-project-docs@antu58-myskills
codex plugin add model-raw-requirements@antu58-myskills
```

更新完成后同样建议创建一个新的 Codex 任务，以加载新版本。

## 卸载

卸载某个 Plugin 会移除其中同名的 Skill，不会影响 Marketplace 中的其他 Plugin。

卸载 `okf-project-docs`：

```bash
codex plugin remove okf-project-docs@antu58-myskills
```

卸载 `model-raw-requirements`：

```bash
codex plugin remove model-raw-requirements@antu58-myskills
```

如果已经卸载所有 Plugin，并且不再需要这个 Marketplace，可以继续移除 Marketplace：

```bash
codex plugin marketplace remove antu58-myskills
```

以后重新使用时，再执行“首次安装”中的 Marketplace 注册命令即可。

## 使用示例

```text
$okf-project-docs 为当前项目创建中文 OKF 文档，并生成可交互 viewer.html。
$model-raw-requirements 将这些零散需求整理为可评审的业务模型。
```

也可以直接描述想要的结果，由 Codex 根据 Skill 的 `description` 自动选择工作流。

## 从旧版 `myskills` Plugin 迁移

早期版本曾将两个 Skill 打包在一个 `myskills` Plugin 中。如果仍安装着旧版，请执行：

```bash
codex plugin marketplace upgrade antu58-myskills
codex plugin remove myskills@antu58-myskills
codex plugin add okf-project-docs@antu58-myskills
codex plugin add model-raw-requirements@antu58-myskills
```

## 维护与新增 Skill

每个 Skill 使用一个同名 Plugin：

```text
plugins/<plugin-name>/.codex-plugin/plugin.json
plugins/<plugin-name>/skills/<skill-name>/SKILL.md
```

新增 Skill 时，在 `.agents/plugins/marketplace.json` 中增加对应 Plugin 条目。更新现有 Skill 时，修改对应 Plugin 内容、更新 Plugin 版本，然后提交并推送 Git。

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
