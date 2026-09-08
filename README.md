# WW.WIKI / Vibecastle

WW.WIKI 是一个面向市场分析、消费者洞察、数据分析与项目推进能力展示的个人品牌站。  
这个版本已经从“静态作品陈列”升级为“可维护的作品集工程”，包含统一视觉系统、项目案例页、真实博客归档，以及可交互的数据可视化组件。

## 当前版本特点

- 全站统一视觉：
  - 网格背景
  - 毛玻璃导航栏
  - 统一圆角、间距、按钮与卡片系统
  - `Plus Jakarta Sans` + `Noto Serif SC` 字体体系
- 四大主导航模块：
  - `/index.html`
  - `/projects.html`
  - `/thoughts.html`
  - `/about.html`
- 项目案例页支持两层交互：
  - tab 切换内容面板
  - 自定义交互看板（matrix / rank）
- 博客与项目结构分离，适合长期维护
- 全站 SEO 基础：每页 description / canonical / Open Graph / Twitter 卡片，
  站点级 robots.txt + sitemap.xml，分享链接自带标题卡与配图
- 移动端汉堡导航、自定义 404 页

## 目录结构

```text
/index.html                         首页
/projects.html                      项目与洞察列表
/thoughts.html                      思考与生活列表
/about.html                         关于我
/404.html                           自定义 404 页
/robots.txt / sitemap.xml           搜索引擎收录配置
/2026/                              博客文章归档
/archive/                           项目案例详情页
/styles/site.css                    全站统一样式
/scripts/project-visuals.js         全站项目交互与图表脚本
/scripts/site-nav.js                移动端汉堡菜单（自动注入，无需每页手写）
/images/og-card.png                 社交分享卡图（1200x630）
/images/favicon.png                 站点图标
/templates/blog-post-template.html  新文章模板（已含 SEO 标签骨架）
/templates/project-case-template.html 新项目模板（已含 SEO 标签骨架）
```

## 如何本地预览

在项目根目录运行一个静态服务即可。Windows 下可用：

```bash
python -m http.server 4174
```

然后打开：

```text
http://127.0.0.1:4174/index.html
```

## 如何新增博客文章

1. 复制 `templates/blog-post-template.html`
2. 放到 `2026/` 目录
3. 修改以下位置：
   - `<title>`
   - `.kicker`
   - `.article-title`
   - `.meta-line`
   - `.rich-text`
4. 按模板里的占位提示，改好 `description`、`canonical`、`og:url` 等标签
5. 把新文章地址加入 `sitemap.xml`
6. 再到 `thoughts.html` 和 `index.html` 增加入口（首页「Latest writing」保持最新 3 篇）

推荐命名：

```text
/2026/日期+标题.html
```

## 如何新增项目案例

1. 复制 `templates/project-case-template.html`
2. 放到 `archive/` 目录
3. 修改以下内容：
   - 项目标题与摘要
   - Hero 区指标卡
   - `Project Snapshot`
   - `Interactive Dashboard`
   - `Interactive View`
   - 底部 JSON 数据源
4. 再到 `projects.html` 和 `index.html` 增加入口

推荐命名：

```text
/archive/project-your-slug.html
```

## 可视化组件怎么维护

项目页的动态图表逻辑在：

```text
/scripts/project-visuals.js
```

当前支持两类：

- `data-chart="matrix"`
  - 用于国家选择、赛道判断、优先级矩阵
- `data-chart="rank"`
  - 用于品类排名、市场规模排序、优先级排序

图表数据不是写死在 JS 里，而是放在页面底部的：

```html
<script type="application/json" id="your-chart-id">
```

这样后续新增项目时，不需要改 JS 逻辑，只需要新增 JSON 数据即可。

## 长期维护建议

- 样式只维护 `styles/site.css`，不要在单页内散写 `<style>`
- 项目交互只维护 `scripts/project-visuals.js`
- 新项目优先复用模板，不要重新发明一套结构
- 每次新增页面后，至少检查：
  - 导航是否一致
  - 跳转是否正常
  - 是否继续引用 `/styles/site.css`
  - 是否继续引用 `/scripts/project-visuals.js`
- 所有文件必须用 UTF-8（无 BOM）保存。曾发生过整页中文变乱码的事故
  （原 UTF-8 被按 GBK 误读再存回），从编辑器导出/粘贴大段中文时尤其注意
- SEO 标签（description / canonical / og）与 `sitemap.xml` 随新页面一起更新，
  分享到微信、飞书、LinkedIn 时会显示标题卡片和配图

## Git 基本流程

```bash
git status
git add .
git commit -m "Describe your update"
git push
```

如果需要新开分支：

```bash
git checkout -b your-branch-name
git push -u origin your-branch-name
```

