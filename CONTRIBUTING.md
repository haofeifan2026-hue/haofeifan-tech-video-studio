# 贡献指南

欢迎提交流程修正、工具适配、质量门槛、可复现脚本和真实失败案例。

## 提交前

1. 先说明具体素材类型、触发条件、当前行为和期望行为。
2. 把工具专属参数放在集成文档或适配层，不写进核心剪辑原则。
3. 不提交客户素材、人物照片、转录、访问令牌、项目 ID、绝对路径或未获授权的参考作品。
4. 新规则必须来自可复现问题；不要把单次审美偏好升级为所有项目的硬性要求。
5. 改变默认行为时更新 `VERSION`、`CHANGELOG.md` 和 `references/upgrading.md`。

## 校验

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests
```

如果修改了视觉脚本，还应查看实际输出图，而不只检查尺寸和退出码。修改时间线或编辑器适配时，必须用真实工程回读轨道、item、字幕和渲染帧。

## Pull Request 内容

- 问题与触发条件
- 最终行为
- 影响的流程阶段
- 验证方式和结果
- 兼容性或迁移说明
