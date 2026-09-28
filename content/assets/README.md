# 资源目录说明

建议把角色素材放在 `content/assets/` 下，并按角色隔离，避免切换角色时资源串用。

```text
content/assets/
├── characters/
│   ├── 苏晚卿/
│   │   ├── portrait.png
│   │   └── expressions/
│   │       ├── normal.png
│   │       ├── smile.png
│   │       ├── sad.png
│   │       ├── angry.png
│   │       └── surprised.png
│   ├── 老李/
│   ├── 吟游诗人/
│   └── 老学者/
└── backgrounds/
    ├── 烟雨楼夜景.jpg
    ├── 城南酒馆.jpg
    ├── 旅人酒馆.jpg
    └── 旧书酒馆.jpg
```

## 文件建议

- `portrait.png`：角色默认立绘，建议透明背���。
- `expressions/*.png`：统一尺寸和命名，插件映射更稳定。
- `backgrounds/*`：建议使用 16:9 图片，避免主体贴近边缘。
- 图片只放入项目资源目录；不要把外部网站的受版权保护素材直接打包发布。

## SillyTavern 使用方式

1. 全局安装 Character Expressions 和 Background Changer。
2. 将每个角色的表情图集单独绑定到角色。
3. 把 `content/sillytavern/ai-tavern-custom.css` 内容粘贴到 Custom CSS。
4. 本地和云端预设分开导入，不要混用。
