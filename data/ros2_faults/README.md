# ROS2 故障数据采集（第一阶段）

从 GitHub 公开页面采集真实故障讨论，供后续数据清洗和问答构建使用。只做基础筛选、按来源去重、格式整理及关键词分类，不开展逐条人工审查，也不生成未经证实的诊断答案。

## 数据范围

- `ros2/ros2`：ROS2 安装、运行与系统集成故障。
- `ros2/rclcpp`：C++ 客户端、Executor、Action、通信和并发问题。
- `ros-navigation/navigation2`：导航、规划、代价地图等问题。
- `ros-controls/ros2_control`：控制器、硬件接口与生命周期问题。

默认每个仓库采集 25 条，共 100 条。查询为 `is:issue is:closed label:bug sort:updated-desc`，按更新日期优先采集；这是首批样本，不是整个 ROS2 生态的全量数据，也不保证覆盖所有发行版。实际数量、时间及失败记录以 `collection_report.json` 为准。

本次使用 GitHub 公共网页中的结构化数据，原因是当前环境不允许访问 `api.github.com`；没有绕过登录或访问私有内容。开发者讨论来自 Issue 评论和关联 PR，不包含独立的 GitHub Discussions 板块。没有采集仿真生成的数据。

## 文件说明

| 路径 | 内容 |
| --- | --- |
| `INDEX.md` | 人工浏览用的案例列表和原文链接 |
| `catalog.csv` | Excel 可打开的案例目录，UTF-8 BOM 编码 |
| `cases.jsonl` | 一行一个案例，统一字段，便于 Python 加载 |
| `raw/issues/<组织>/<仓库>/<编号>.json` | Issue 原文、评论原文、页面可获取的时间线和关联 PR 元数据 |
| `raw/pull_requests/<组织>/<仓库>/<编号>.json` | 关联 PR 的页面正文、讨论文本和提交链接 |
| `raw/pull_requests/<组织>/<仓库>/<编号>.patch` | 对应 PR 的代码变更补丁；获取失败会记录原因 |
| `raw/pull_requests/<组织>/<仓库>/<编号>.changes.json` | 完整补丁不可访问时，从文件变更页面提取的代码片段 |
| `collection_report.json` | 本次查询、采集数量、评论完整性及失败报告 |

## 统一字段

`fault_phenomenon` 保存标题和 Issue 正文；`error_logs` 提取含错误关键词的原文行；`code_and_log_blocks` 保存 Markdown 代码块。**代码块可能是配置、复现代码或终端输出，并不全部是错误日志。** 每个提取项保留来源链接。

`fault_cause`、`troubleshooting_steps`、`solution`、`verification_result` 暂为 `null`，交由第二阶段根据证据补充。`solution_evidence_candidates` 只是出现 fixed、resolved、workaround 等关键词的评论原文，`verified=false`，不代表已确认方案。修复信息还可查看关联 PR 和补丁。

`category_hints` 是多标签关键词粗分类；`ros_distro_mentions` 只是发行版名称在讨论中出现，不代表已确认运行环境。`review_status=unreviewed`、`training_ready=false` 表示这些是采集材料，不是可直接微调的标注答案。

评论按时间线事件 ID 去重，案例按来源 URL 去重。比较 `comment_count_collected` 与 `comment_count_expected` 判断是否完整，`comments_complete=false` 的记录需后续补采或保留为部分数据。PR 页面可能折叠讨论，其 `discussion_complete=null`，不宣称全部评论已采集。不会把 Issue 关闭或 PR 合并当作用户已验证解决。

原始材料保留公开作者账号与原文内容；本阶段未进行系统脱敏。原始日志或补丁可能含公开邮箱、用户名和机器路径，第二阶段对训练数据统一处理即可。来源归属仍属于原作者／上游项目；仓库代码许可证不能自动视作所有讨论文本的训练许可。

本次环境拦截完整补丁下载，因此优先保留 PR 正文、提交链接以及 `.changes.json` 中的可见代码变更。网页可能折叠大文件或部分差异，`complete=null`；这些片段不等同于完整、可应用的 Git 补丁。失败项仍保留在报告中，不会用空文件代替下载成功。

## 重新采集或扩量

在仓库根目录运行，Python 3.10+，无需第三方包：

```bash
python scripts/collect_ros2_faults.py
```

扩大采集量时建议指定新的输出目录，保留首批快照：

```bash
python scripts/collect_ros2_faults.py --per-repo 100 --max-pages 10 --output data/ros2_faults_batch2
```

缓存默认位于 `/tmp/ros2-fault-collector-cache`，可断点恢复。使用相同缓存会复用已采集页面；要重新获取最新页面，指定新的 `--cache` 目录。默认同时最多两个工作线程，请求间隔至少 0.5 秒，遇到限流会有限重试，持续失败会记录错误。

同一输出目录中的原始文件用于续采，会保留旧文件；本轮数据范围以本轮 `cases.jsonl` 和 `collection_report.json` 为准。原始文件的 `source` 保存 URL、抓取时间、HTTP 状态和响应 SHA-256；哈希是响应指纹，不是完整 HTML 存档，完整页面响应仅保存在本机缓存中。

脚本退出码 1 表示有 Issue 采集失败或某项目未达到目标条数；关联 PR／补丁的失败在报告中单独列出。GitHub 改变页面结构时会报错，不会写入登录页面冒充案例。

第二阶段应按 Issue 与关联 PR 的关系分组后再划分训练／验证／测试集，避免同一故障讨论和修复记录跨集合泄漏。
