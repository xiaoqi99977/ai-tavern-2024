# 角色卡、世界书与预设

本目录提供 AI 酒馆的第一批可编辑内容模板。

## 文件

- `characters/*.json`：四张角色卡，字段可直接改写。
- `lorebook/ai-tavern-world.json`：酒馆、城镇和人物关系条目。
- `presets/local-completion-rp.json`：本地 KoboldCpp/Ollama Completion 参数。
- `presets/cloud-compliant-rp.json`：云端 API 的合规叙事参数。
- `sillytavern/ai-tavern-custom.css`：全局磨砂暗调 CSS。
- `assets/README.md`：立绘、表情和背景目录规划。

## 导入原则

- 角色卡是角色独立内容；预设是全局生成配置。
- 本地预设与云端预设必须分开使用。
- JSON 模板不绑定具体插件版本；导入 SillyTavern 前，按当前版本的字段映射检查一次。
- 云端配置不用于规避安全策略；涉及不适合生成的内容时，应修改创作请求。
