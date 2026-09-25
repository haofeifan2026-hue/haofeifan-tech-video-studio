# Haofeifan Tech Video Studio

[![Validate](https://github.com/haofeifan2026-hue/haofeifan-tech-video-studio/actions/workflows/validate.yml/badge.svg)](https://github.com/haofeifan2026-hue/haofeifan-tech-video-studio/actions/workflows/validate.yml)
[![Version](https://img.shields.io/badge/version-1.0.0-35d0aa.svg)](https://github.com/haofeifan2026-hue/haofeifan-tech-video-studio/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/license-MIT-f5b948.svg)](LICENSE)

一套面向 Codex 的开源科技口播剪辑 Skill。它把素材盘点、语义粗剪、字幕、内容补画、科技感包装、BGM、真人封面和质量验收整理成一条可重复、可升级的制作流程。

The project is a reusable Codex skill for polished, human-first technology talking-head videos.

## 核心原则

- 真人和观点是主角，科技感只负责解释、分层和引导注意力。
- 实际音频转录是时间真相，脚本只用于结构和术语参考。
- B-roll 必须能映射到当前口播原句，并记录来源、时间和画面作用。
- 先锁定 A-roll，再做字幕、补画、包装、BGM 和封面。
- 新风格先复制时间线，不覆盖已经批准的基础版本。
- 只有经过时间线回读、组合帧检查和媒体 QA 的内容才能报告完成。

## 能做什么

- 分析单人口播、访谈、教程、屏幕录制和参考视频。
- 识别重复 take、重录、口误、无效停顿和不完整句子。
- 生成短语级中文字幕并保护人脸、嘴、手势和关键 UI。
- 根据最终口播补充真实截图、信息图、图片或短视频。
- 添加克制的 HUD、章节条、关键词强调和全屏信息场景。
- 选择或生成内容匹配的无人声 BGM，并在人声下自动 duck。
- 从视频真人帧制作同一视觉系统的竖屏科技封面。
- 输出可编辑工程、制作记录、封面和可验证的验收报告。

## 安装

需要 Codex 桌面端或支持本地 Skills 的 Codex 环境。克隆本仓库后执行：

```bash
git clone https://github.com/haofeifan2026-hue/haofeifan-tech-video-studio.git
cd haofeifan-tech-video-studio
./scripts/install.sh
```

默认安装到 `${CODEX_HOME:-$HOME/.codex}/skills/haofeifan-tech-video-studio`。指定其它目录：

```bash
./scripts/install.sh --target /path/to/codex/skills/haofeifan-tech-video-studio
```

重启或刷新 Codex 后，可以显式调用：

```text
用 $haofeifan-tech-video-studio 分析并剪辑这些口播素材。
```

Skill 允许自动发现，因此直接说“把这批口播剪成科技感竖屏短视频”也可以触发。

## 可选依赖

核心 Skill 不绑定某一家剪辑软件。不同能力按需启用：

| 能力 | 推荐工具 | 是否必需 |
|---|---|---|
| 可编辑粗剪、字幕和素材放置 | ChatCut | 否 |
| 高级 HTML 动效与混音 | HyperFrames | 否 |
| 组件化视频模板 | Remotion | 否 |
| 位图封面与写实补画 | ImageGen 或本地图像工具 | 否 |
| 媒体探测、响度与转码 | ffmpeg / ffprobe | 建议 |
| 竖屏图片适配脚本 | Python 3.10+、Pillow | 使用脚本时需要 |

完整的能力路由见 [工具与 Skill 集成](references/integrations.md)。安装脚本只安装本 Skill，不会自动安装第三方服务、插件或付费模型。

## 使用方式

### 1. 只分析，不修改

```text
先分析这批素材和参考视频，给出风格指纹、take 选择、风险和剪辑计划，不要修改时间线。
```

### 2. 完整剪辑

```text
用这套流程直接剪成 9:16 科技口播：清理重录和口误，做字幕、相关 B-roll、轻科技包装、无人声 BGM 和真人封面，保留可编辑工程。
```

### 3. 接手已有时间线补画

```text
不要重剪已经锁定的 A-roll。根据最终字幕找出需要视觉解释的段落，优先用项目已有素材，再补充相关图片或短视频并验证每个插入点。
```

### 4. 只做封面

```text
从视频中挑选清晰、睁眼的真人帧，提炼 3 到 8 个字的核心标题，制作 1080x1920 科技封面并检查 270x480 缩略图。
```

更多调用示例和制作 brief 见 [examples](examples/README.md)。

## 工作流

```mermaid
flowchart LR
    A[素材与参考盘点] --> B[风格指纹]
    B --> C[A-roll 结构锁定]
    C --> D[字幕]
    D --> E[内容补画]
    E --> F[科技感包装]
    F --> G[BGM 与混音]
    G --> H[真人封面]
    H --> I[时间线与媒体 QA]
```

完整阶段要求见 [端到端制作流程](references/end-to-end-production.md)，质量底线见 [质量门槛](references/quality-gates.md)。

## 仓库结构

```text
.
|-- SKILL.md
|-- agents/openai.yaml
|-- references/
|   |-- end-to-end-production.md
|   |-- content-driven-broll.md
|   |-- quality-gates.md
|   |-- style-presets.md
|   |-- integrations.md
|   `-- upgrading.md
|-- scripts/
|   |-- compose_vertical_still.py
|   |-- install.sh
|   `-- validate_repo.py
|-- examples/
|-- tests/
`-- .github/workflows/validate.yml
```

## 本地校验

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests
```

如果本机有 Codex 内置的 `skill-creator`，还可以运行其 `quick_validate.py` 检查 Skill frontmatter 和目录结构。

## 升级与贡献

升级遵循语义化版本。任何修改都必须保留转录时间真相、原素材不覆盖、内容相关性、真人保护和可验证交付等核心不变量。详情见 [升级指南](references/upgrading.md) 和 [贡献指南](CONTRIBUTING.md)。

## 许可证

[MIT](LICENSE)
