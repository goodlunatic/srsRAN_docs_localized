# srsRAN Docs Localized

这是一个本地整理版的 `srsRAN` 文档仓库，目标是把以下三部分内容放在同一个工作目录里统一预览：

- `srsran_docs`：文档主页和公共入口页
- `srsran_project`：srsRAN Project 文档
- `srsran_4g`：srsRAN 4G 文档

目前仓库提供了一个轻量本地服务，把这三个部分合并成两套语言入口：

- 英文文档入口：`http://127.0.0.1:8081/`
- 中文文档入口：`http://127.0.0.1:8082/`

## 项目结构

```text
srsRAN_docs_localized/
├── README.md
├── serve_localized_docs.py
├── run_localized_docs.sh
├── srsran_docs/
├── srsran_project/
└── srsran_4g/
```

各目录作用如下：

- `srsran_docs/`
  - 主页文档源目录
  - 包含英文 `docs/source/` 和中文 `docs/source_zh/`
- `srsran_project/`
  - srsRAN Project 的静态 HTML 文档
  - 包含 `en/` 和 `zh/`
- `srsran_4g/`
  - srsRAN 4G 的静态 HTML 文档
  - 包含 `en/` 和 `zh/`
- `serve_localized_docs.py`
  - 本地统一入口服务
  - 负责把主页、Project 文档、4G 文档整合到同一个访问入口下

## 合并后的访问方式

启动服务后，会提供两个端口：

- `8081`：英文入口
- `8082`：中文入口

每个端口下的主要路由如下：

- `/`
  - 当前语言的统一主页
- `/project/`
  - 跳转到当前语言的 `srsran_project` 文档
- `/4g/`
  - 跳转到当前语言的 `srsran_4g` 文档
- `/feature.html`
  - `srsran_docs` 中的功能页
- `/reporting_issues.html`
  - 英文问题反馈页
- `/page_1.html`
  - 中文问题反馈页

示例：

- 英文主页：`http://127.0.0.1:8081/`
- 英文 Project：`http://127.0.0.1:8081/project/`
- 英文 4G：`http://127.0.0.1:8081/4g/`
- 中文主页：`http://127.0.0.1:8082/`
- 中文 Project：`http://127.0.0.1:8082/project/`
- 中文 4G：`http://127.0.0.1:8082/4g/`

## 运行方式

要求：

- Python 3

在项目根目录执行：

```bash
python3 serve_localized_docs.py
```

或者：

```bash
bash run_localized_docs.sh
```

启动后终端会输出：

```text
en docs: http://127.0.0.1:8081/
zh docs: http://127.0.0.1:8082/
```

按 `Ctrl+C` 停止服务。

## 实现说明

这个仓库没有把三个站点重新打包成一个新的 Sphinx 工程，而是采用了更轻量的方式：

- 保留 `srsran_project` 和 `srsran_4g` 现有静态 HTML 目录
- 用 `serve_localized_docs.py` 提供统一首页
- 根据端口区分语言
- 根据路径把请求映射到对应的静态文档目录

这样做的好处是：

- 不需要重建已有静态文档
- 不会破坏原有文档目录结构
- 本地预览简单
- 中英文入口清晰

## 后续可做的事

如果还要继续完善，这个仓库后面可以再做：

- 把主页改成更接近官方文档站样式
- 把主页中的更多入口页接到本地文档
- 补充中文主页内容
- 增加自动启动脚本或反向代理配置

## 备注

如果你看到仓库里还有其他未跟踪文件或子仓库状态变化，那些不是这个 README 改动的一部分；当前 README 只描述本地统一预览这套方案。
