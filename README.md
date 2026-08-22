# data-export-approver
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/data-export-approver)

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/data-export-approver.svg)](https://pypi.org/project/data-export-approver/)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://pep8.org/)

🔒 Enforce approval workflows for Pandas data exports — stop unauthorized `df.to_csv()` in production.

---

## Features

- **Auto-activate** — Works immediately upon import, zero configuration required
- **Comprehensive coverage** — Intercepts 14 Pandas export methods (`to_csv`, `to_excel`, `to_json`, etc.)
- **Visual feedback** — Red lock / green release prompts powered by the `rich` library
- **Flexible configuration** — Manage approval codes via environment variables or config file
- **Zero-intrusion** — No changes to existing code; enable/disable at will

## Quick Start

### Installation

```bash
pip install data-export-approver
```

Or with Poetry:

```bash
poetry add data-export-approver
```

### Basic Usage

```python
import data_export_approver  # Auto-activates on import
import pandas as pd

df = pd.DataFrame({'sensitive_data': [1, 2, 3]})
df.to_csv('output.csv')  # 🔒 Triggers approval prompt
```

When an export is attempted, a red security alert appears:

```
╭─────────────── ⚠ SECURITY ALERT ⚠ ───────────────╮
│ 🔒 UNAUTHORIZED DATA EXPORT ATTEMPT              │
│                                                   │
│ Method: to_csv                                   │
│ Status: BLOCKED - Approval Required              │
╰───────────────────────────────────────────────────╯
Enter approval code to proceed: _
```

After entering a valid approval code:

```
╭─────────────── ✓ AUTHORIZED ✓ ───────────────────╮
│ ✅ APPROVAL GRANTED                               │
│                                                   │
│ Method: to_csv                                   │
│ Status: Executing export...                      │
╰───────────────────────────────────────────────────╯
```

## Usage Guide

### Configure Approval Codes

**Method 1: Environment Variable**

```bash
export DATA_EXPORT_APPROVAL_CODES="TICKET-12345,TICKET-67890,EMERGENCY-001"
```

**Method 2: Config File**

Create `~/.data-export-approver.json`:

```json
{
  "approval_codes": [
    "TICKET-12345",
    "TICKET-67890",
    "EMERGENCY-001"
  ]
}
```

**Method 3: CLI Tool**

```bash
# Add an approval code
python -m data_export_approver config --add TICKET-12345

# View current configuration
python -m data_export_approver config --show

# Test that the patch is active
python -m data_export_approver test
```

### Manual Control

```python
import data_export_approver

# Temporarily disable approval
data_export_approver.disable()

df.to_csv('output.csv')  # No approval required

# Re-enable
data_export_approver.enable()
```

### Conditional Activation

```python
import os
import data_export_approver

# Enable only in production
if os.getenv('ENVIRONMENT') == 'production':
    data_export_approver.enable()
else:
    data_export_approver.disable()
```

### Supported Export Methods

| Method | Target |
|---|---|
| `to_csv` | CSV files |
| `to_excel` | Excel files |
| `to_json` | JSON files |
| `to_parquet` | Parquet files |
| `to_pickle` | Pickle files |
| `to_sql` | SQL databases |
| `to_hdf` | HDF5 files |
| `to_feather` | Feather files |
| `to_stata` | Stata files |
| `to_gbq` | Google BigQuery |
| `to_html` | HTML files |
| `to_xml` | XML files |
| `to_markdown` | Markdown files |
| `to_clipboard` | System clipboard |

## Project Structure

```
data-export-approver/
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── publish.yml
├── src/
│   └── data_export_approver/
│       ├── __init__.py       # Auto-activation entry point
│       ├── __main__.py       # CLI entry point
│       ├── cli.py            # CLI commands
│       ├── core.py           # Core monkey-patching logic
│       └── utils.py          # Utilities
├── tests/
├── LICENSE
├── README.md
└── pyproject.toml
```

## Tech Stack

- **Python** 3.8+
- **[Pandas](https://pandas.pydata.org/)** — Intercept target
- **[rich](https://github.com/Textualize/rich)** — Terminal UI
- **[Poetry](https://python-poetry.org/)** — Package management

## How It Works

1. **Monkey Patching** — Replaces Pandas DataFrame export methods on import
2. **Method Wrapping** — Uses `functools.wraps` to preserve original method signatures
3. **Approval Gate** — Requests and validates an approval code before executing the export
4. **Transparent Pass-through** — Calls the original method and returns its result after validation

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.
Copyright 2026 Chance Dean — novelnexusai@outlook.com

---

## 中文文档

🔒 强制审批流程的 Pandas 数据导出管控工具 — 阻止生产环境中未授权的 `df.to_csv()` 操作。

---

### 核心特性

- **自动激活** — 导入即生效，无需额外配置
- **全面覆盖** — 劫持 14 个 Pandas 导出方法（`to_csv`、`to_excel`、`to_json` 等）
- **视觉化反馈** — 使用 `rich` 库提供红色锁定 / 绿色放行的直观效果
- **灵活配置** — 支持环境变量和配置文件两种方式管理审批码
- **零侵入** — 不修改原有代码逻辑，可随时启用/禁用

### 快速开始

#### 安装

```bash
pip install data-export-approver
```

或使用 Poetry：

```bash
poetry add data-export-approver
```

#### 基本使用

```python
import data_export_approver  # 导入即自动激活
import pandas as pd

df = pd.DataFrame({'sensitive_data': [1, 2, 3]})
df.to_csv('output.csv')  # 🔒 触发审批提示
```

### 使用指南

#### 配置审批码

**方法 1：环境变量**

```bash
export DATA_EXPORT_APPROVAL_CODES="TICKET-12345,TICKET-67890,EMERGENCY-001"
```

**方法 2：配置文件**

创建 `~/.data-export-approver.json`：

```json
{
  "approval_codes": [
    "TICKET-12345",
    "TICKET-67890",
    "EMERGENCY-001"
  ]
}
```

**方法 3：CLI 工具**

```bash
# 添加审批码
python -m data_export_approver config --add TICKET-12345

# 查看当前配置
python -m data_export_approver config --show

# 测试补丁是否生效
python -m data_export_approver test
```

#### 手动控制

```python
import data_export_approver

# 临时禁用审批
data_export_approver.disable()

df.to_csv('output.csv')  # 无需审批

# 重新启用
data_export_approver.enable()
```

#### 使用场景

**场景 1：生产环境数据保护**

```python
import data_export_approver

df = load_sensitive_data()
df.to_csv('export.csv')  # 需要输入审批码
```

**场景 2：结合工单系统审计追踪**

```bash
export DATA_EXPORT_APPROVAL_CODES="JIRA-12345,JIRA-67890"
```

**场景 3：开发环境豁免**

```python
import os
import data_export_approver

if os.getenv('ENV') == 'development':
    data_export_approver.disable()
```

### 工作原理

1. **Monkey Patching** — 在导入时自动替换 Pandas DataFrame 的导出方法
2. **方法包装** — 使用 `functools.wraps` 保持原始方法签名
3. **审批拦截** — 在执行原始方法前，先请求并验证审批码
4. **透明传递** — 验证通过后，调用原始方法并返回结果

### 常见问题

**Q: 会影响性能吗？**
A: 影响极小。仅在导出操作时增加一次审批验证，不影响数据处理性能。

**Q: 可以绕过审批吗？**
A: 可以通过 `disable()` 方法禁用，但这需要修改代码。建议在生产环境中通过权限控制防止代码修改。

**Q: 支持其他数据处理库吗？**
A: 当前仅支持 Pandas。未来可能扩展到其他库（如 Polars、Dask 等）。

**Q: 审批码存储安全吗？**
A: 审批码存储在本地配置文件或环境变量中。建议使用工单系统生成的临时审批码，而非固定密码。

### 许可证

Apache License 2.0 — 详见 [LICENSE](LICENSE)。
Copyright 2026 Chance Dean — novelnexusai@outlook.com
