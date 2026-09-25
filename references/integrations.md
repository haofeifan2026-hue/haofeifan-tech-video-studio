# 工具与 Skill 集成

核心流程按能力选择工具，不要求同时安装全部集成。每次只加载当前阶段需要的 Skill；缺少某项能力时，说明可完成范围和未验证项，不伪造可编辑工程或渲染结果。

## 能力路由

| 阶段 | 优先能力或 Skill | 何时使用 | 可接受替代 |
|---|---|---|---|
| Skill 维护 | `skill-creator` | 创建、更新和校验本 Skill | 手工维护并运行 `scripts/validate_repo.py` |
| ChatCut 会话 | `chatcut:chatcut-plugin-basics` | 使用 Hosted ChatCut 前读取连接、项目和编辑约定 | 其它支持可编辑时间线的编辑器 |
| 口播剪辑 | `chatcut:talking-head-guide` | 单人、多人口播、访谈、教程的结构剪辑 | 具备转录和帧级时间线的 NLE |
| 转录与字幕 | `chatcut:transcription` | 转录、修复、字幕生成和刷新 | Whisper 等带时间码转录加 NLE 字幕轨 |
| 本地素材导入 | `chatcut:asset-import` | 把本地图片、音频和视频放进 Hosted ChatCut 项目 | 编辑器原生导入 |
| 音乐 | `chatcut:music` | 生成原创无人声 BGM 或歌曲 | 用户授权音乐或其它生成器 |
| 视频补画 | `chatcut:video-gen` | 静态画面不能表达动作或过程时 | 实拍、屏录、图片加轻推近 |
| 滤镜与转场 | `chatcut:shader-gen` | 内置效果不能满足明确视觉任务时 | 编辑器内置效果 |
| 时间线验证 | `chatcut:verification` | Hosted ChatCut 编辑完成后回读与抽帧 | 编辑器结构导出加本地帧检查 |
| 导出 | `chatcut:export` | 用户明确要求视频、音频、字幕或 XML 导出 | 当前编辑器原生导出 |
| 端到端高级包装 | `chatcut-hyperframes-auto-editor` | ChatCut 粗剪后继续做 HTML 动效、混音和渲染 | 分别使用 ChatCut 与 HyperFrames |
| HTML 动效 | `hyperframes:hyperframes` | 标题、字幕、音频响应、复杂信息场景 | 编辑器 MG 或 Remotion |
| GSAP 动画 | `hyperframes:gsap` | HyperFrames 中需要时间线、缓动和 stagger | CSS/Web Animations |
| HyperFrames CLI | `hyperframes:hyperframes-cli` | lint、inspect、preview、render 和 doctor | 对应本地工具 |
| React 视频模板 | `remotion:remotion-best-practices` | 需要可复用组件、严格布局和批量渲染 | HyperFrames 或编辑器模板 |
| 位图生成 | `imagegen` | 封面、写实补画、背景处理或参考图变体 | 本地图像工具、实拍、图库 |

## 选择规则

1. 先判断当前任务是分析、剪辑、补画、音频、封面还是导出，不因为工具存在就全部调用。
2. 可编辑时间线优先交给 NLE；复杂 HTML 动效和渲染交给 HyperFrames；批量组件模板交给 Remotion；位图交给 ImageGen 或本地图像工具。
3. 真实产品、真实界面和真实人物优先使用用户素材或可核验截图。生成内容不得伪装成产品现状或真实新闻画面。
4. 付费生成按实际模型调用处理。用户已明确授权具体生成时执行；范围不明确时先固定数量、时长、比例和内容。
5. 导出、发布和覆盖原文件是独立阶段。完成时间线不代表已经导出，生成素材不代表已经放进成片。

## ChatCut 轨道约定

- A-roll 和旁白轨设为 `anchor`。
- BGM 和持续环境音乐轨设为 `follower`。
- 短促 SFX 通常不参与 ducking。
- B-roll、科技包装和字幕各用独立轨道，便于关闭、替换和验证。
- 所有编辑后回读 item 的起止帧、轨道、淡化、效果和可见性。

## 可移植性边界

不同环境中的 Skill 名称、工具参数和计费方式可能变化。集成名称只用于能力发现，核心工作流不得依赖某个临时项目 ID、绝对路径、私有提示词或单一供应商的返回结构。工具不可用时保留分析、剪辑决策表、素材映射和 QA 记录，并明确哪些操作尚未执行。
