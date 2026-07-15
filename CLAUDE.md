# 个人笔记网站 - 项目记忆文档

## 📋 项目概述

这是一个基于 GitHub Pages 的个人笔记网站，支持 Markdown 渲染、大纲导航、搜索功能等，具有高度可扩展性。

### 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| HTML5 | - | 页面结构 |
| CSS3 | - | 样式设计 |
| JavaScript | ES6+ | 交互逻辑 |
| marked.js | 12.0.0 | Markdown 渲染 |
| highlight.js | 11.9.0 | 代码高亮 |
| Font Awesome | 6.5.1 | 图标 |

### 核心功能

- ✅ 笔记目录导航（左侧）
- ✅ Markdown 渲染
- ✅ 代码语法高亮
- ✅ 图片显示
- ✅ 搜索功能
- ✅ 阅读历史（前进/后退）
- ✅ 大纲导航（右侧）
- ✅ 响应式设计

---

## 📁 项目结构

```
个人网站github/
├── index.html          # 主页面（包含所有样式和脚本）
├── notes-config.js     # 笔记配置文件（自动生成）
├── build-config.py     # 配置生成脚本
├── fix-images.py       # 图片路径修复脚本
├── 启动预览.bat        # 本地预览启动脚本
├── .gitignore          # Git 忽略规则
└── [笔记模块文件夹]/   # 笔记模块（动态添加）
    ├── 笔记文件.md      # Markdown 笔记
    └── assets/         # 图片资源（可选）
```

---

## 🔧 核心文件说明

### 1. index.html

主页面，包含：
- 左侧侧边栏：笔记目录和搜索框
- 中间内容区：Markdown 渲染区域
- 右侧大纲面板：自动提取标题生成导航
- 顶部工具栏：面包屑、前进/后退按钮

### 2. notes-config.js

笔记配置文件，由 `build-config.py` 自动生成：
```javascript
const notesConfig = [
    {
        "name": "模块名称",
        "type": "folder",
        "children": [
            {
                "name": "笔记标题",
                "type": "file",
                "path": "模块名称/笔记文件.md"
            }
        ]
    }
];
```

### 3. build-config.py

扫描项目目录，自动生成 `notes-config.js`：
- 忽略隐藏文件夹和特殊文件夹（node_modules, dist, build）
- 支持中文文件夹名和文件名
- 自动识别 `.md` 文件

### 4. fix-images.py

修复 Markdown 中的图片路径：
- 将 Windows 绝对路径 `C:\Users\...` 转换为相对路径 `./assets/`
- 自动复制图片到对应模块的 `assets` 目录

### 5. 启动预览.bat

一键启动本地预览：
- 运行 `build-config.py` 生成配置
- 启动 Python HTTP 服务器（端口 8080）
- 自动打开浏览器

---

## 🚀 新增笔记步骤

### 方式一：简单方式（推荐）

1. 将笔记文件夹复制到项目根目录
2. 双击运行 `启动预览.bat`
3. 本地预览确认效果
4. 推送到 GitHub：
   ```bash
   git add .
   git commit -m "添加新笔记模块"
   git push origin main
   ```

### 笔记文件夹结构要求

```
笔记模块名称/
├── 笔记文件名.md      # Markdown 文件（可多个）
└── assets/           # 图片文件夹（可选）
    └── image-xxx.png # 笔记中引用的图片
```

---

## 📝 图片路径规范

### 正确写法

```markdown
<!-- Markdown 格式 -->
![图片描述](./assets/image-xxx.png)

<!-- HTML 格式 -->
<img src="./assets/image-xxx.png" alt="图片描述" />
```


## 🌐 GitHub Pages 部署

### 仓库信息

- **仓库地址**: `https://github.com/a123139/note`
- **网站地址**: `https://a123139.github.io/note/`
- **分支**: `main`


## 🔍 搜索功能

- 在左侧搜索框输入关键词
- 实时过滤笔记标题
- 匹配的笔记高亮显示

---

## 📑 大纲导航

- 打开笔记时自动提取 H1-H6 标题
- 点击大纲项跳转到对应位置
- 滚动页面时自动高亮当前位置

---

## 📱 响应式设计

- 桌面端：三栏布局（目录 + 内容 + 大纲）
- 平板端：自适应布局
- 移动端：侧边栏折叠，底部导航
