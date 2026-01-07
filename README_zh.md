# 网络监控检测工具 (Network Monitoring Detection Tool)

一个用于检测系统是否存在网络监控的Python工具。该工具可以帮助识别代理设置、抓包工具、可疑网络连接以及潜在的中间人攻击。

## 功能特性

- **代理检测**: 检查系统和环境变量中的代理配置
- **进程监控**: 识别常见的网络抓包和监控工具（如 Wireshark, Fiddler, Charles）
- **网络接口分析**: 检测虚拟网络适配器和VPN连接
- **连接分析**: 检查可疑的监听端口和活动连接
- **证书检测**: 测试TLS/SSL连接以发现潜在的中间人攻击
- **双语支持**: 支持中文和英文输出
- **彩色终端输出**: 清晰的风险等级展示
- **JSON导出**: 支持将检测结果导出为JSON格式

## 系统要求

- Python 3.6+
- Windows / Linux / macOS

## 安装

### 1. 克隆或下载项目

```bash
cd check-internet-monitor
```

### 2. 安装依赖

使用 conda 环境（推荐）:

```bash
conda activate stock_api
pip install -r requirements.txt
```

或使用 pip:

```bash
pip install -r requirements.txt
```

## 语言支持

本工具支持双语输出：

- **中文**（默认）: `python main.py` 或 `python main.py --lang zh`
- **English（英文）**: `python main.py --lang en`

您也可以通过环境变量设置默认语言：

```bash
# Linux/Mac
export NETWORK_MONITOR_LANG=en

# Windows
set NETWORK_MONITOR_LANG=en
```

## 使用方法

### 基本用法

运行所有检测（中文输出，默认）：

```bash
python main.py
```

使用英文输出：

```bash
python main.py --lang en
```

### 快速模式

跳过耗时的证书检测：

```bash
python main.py --quick
```

### 导出结果

将检测结果导出为JSON文件：

```bash
python main.py --json report.json
```

### 命令行选项

```
usage: main.py [-h] [--json FILE] [--quick] [--lang {zh,en}]

检测系统上的网络监控和监视

可选参数:
  -h, --help         显示帮助信息并退出
  --json FILE        将结果导出到JSON文件
  --quick            跳过缓慢的检查(证书验证)
  --lang {zh,en}     输出语言 (zh=中文, en=英文)
```

## 检测模块说明

### 1. 代理检测 (Proxy Detection)

检查以下项目：
- 环境变量中的代理设置（HTTP_PROXY, HTTPS_PROXY等）
- Windows系统代理配置（注册表）
- 自动代理配置URL

**风险等级**: MEDIUM - 如果检测到代理配置

### 2. 进程检测 (Process Detection)

扫描以下类型的进程：
- 数据包捕获工具: Wireshark, TShark, TCPDump
- 代理和调试工具: Fiddler, Charles, Burp Suite, mitmproxy
- 网络监控工具: NetworkMiner, Ettercap
- 企业监控软件: ActivTrak, Teramind, InterGuard

**风险等级**: HIGH - 如果检测到监控工具进程

### 3. 网络接口检测 (Network Interface Detection)

检查：
- 虚拟网络适配器（可能表示VPN或虚拟机）
- VPN连接（通过常见VPN端口检测）

**风险等级**: MEDIUM - 如果检测到虚拟适配器或VPN

### 4. 连接分析 (Connection Analysis)

分析：
- 可疑的监听端口（代理端口8080, 8888, 3128等）
- 建立的网络连接
- 连接到单个IP的异常多连接
- 网络统计信息

**风险等级**: MEDIUM - 如果检测到可疑端口或连接

### 5. 证书检测 (Certificate Detection)

测试：
- 连接到知名网站（Google, GitHub）
- 检查证书颁发者是否可疑
- 识别自签名证书（可能是中间人攻击）
- 检测企业代理证书（Zscaler, BlueCoat等）

**风险等级**: HIGH - 如果检测到可疑证书或MITM迹象

## 输出示例

```
======================================================================
Network Monitoring Detection Report
Generated: 2024-01-15 10:30:45
======================================================================

Overall Risk Level: HIGH

[Proxy Detection]
  Risk Level: MEDIUM
  Findings: 1
    1. [MEDIUM] Environment Proxy: HTTP_PROXY=http://proxy.company.com:8080

[Process Detection]
  Risk Level: HIGH
  Findings: 1
    1. [HIGH] Suspicious Process: Wireshark (Packet Analyzer) (PID: 1234, Name: wireshark.exe)

...
```

## 注意事项

1. **权限要求**: 某些检测功能可能需要管理员权限才能获得完整结果
2. **误报可能**: 某些发现可能是合法的（如企业VPN、安全软件等）
3. **结果解读**: 请根据实际情况判断检测结果的含义
4. **网络连接**: 证书检测模块需要互联网连接

## 免责声明

此工具仅用于合法的安全检查和教育目的。请确保您有权在目标系统上运行此工具。作者不对工具的误用承担任何责任。

## 技术栈

- **psutil**: 系统和进程信息
- **colorama**: 彩色终端输出
- **requests**: HTTP请求（未来扩展用）
- **ssl/socket**: TLS证书检测

## 项目结构

```
check-internet-monitor/
├── main.py                    # 主入口脚本
├── detectors/
│   ├── __init__.py
│   ├── proxy_detector.py      # 代理检测模块
│   ├── process_detector.py    # 进程检测模块
│   ├── network_detector.py    # 网络接口检测模块
│   ├── connection_detector.py # 连接分析模块
│   └── certificate_detector.py # 证书检测模块
├── utils/
│   ├── __init__.py
│   └── reporter.py            # 报告生成工具
├── requirements.txt           # 依赖列表
└── README.md                  # 本文档
```

## 贡献

欢迎提交问题报告和功能请求！

## 许可证

MIT License

## 作者

Created for educational and security research purposes.
