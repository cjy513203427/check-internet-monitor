# Network Monitoring Detection Tool

A Python tool for detecting network monitoring on your system. This tool helps identify proxy settings, packet capture tools, suspicious network connections, and potential man-in-the-middle attacks.

## Features

- **Proxy Detection**: Check proxy configurations in system and environment variables
- **Process Monitoring**: Identify common network packet capture and monitoring tools (e.g., Wireshark, Fiddler, Charles)
- **Network Interface Analysis**: Detect virtual network adapters and VPN connections
- **Connection Analysis**: Check for suspicious listening ports and active connections
- **Certificate Detection**: Test TLS/SSL connections to discover potential man-in-the-middle attacks
- **Bilingual Support**: Supports Chinese and English output
- **Colored Terminal Output**: Clear risk level display
- **JSON Export**: Export detection results to JSON format

## System Requirements

- Python 3.6+
- Windows / Linux / macOS

## Installation

### 1. Clone or Download the Project

```bash
cd check-internet-monitor
```

### 2. Install Dependencies

Using conda environment (recommended):

```bash
conda activate stock_api
pip install -r requirements.txt
```

Or using pip:

```bash
pip install -r requirements.txt
```

## Language Support

This tool supports bilingual output:

- **Chinese (中文)** (default): `python main.py` or `python main.py --lang zh`
- **English**: `python main.py --lang en`

You can also set the default language using an environment variable:

```bash
# Linux/Mac
export NETWORK_MONITOR_LANG=en

# Windows
set NETWORK_MONITOR_LANG=en
```

## Usage

### Basic Usage

Run all detections (Chinese output, default):

```bash
python main.py
```

Use English output:

```bash
python main.py --lang en
```

### Quick Mode

Skip time-consuming certificate detection:

```bash
python main.py --quick
```

Or with English output:

```bash
python main.py --lang en --quick
```

### Export Results

Export detection results to JSON file:

```bash
python main.py --json report.json
```

### Command Line Options

```
usage: main.py [-h] [--json FILE] [--quick] [--lang {zh,en}]

Detect network monitoring and surveillance on your system

optional arguments:
  -h, --help         show this help message and exit
  --json FILE        Export results to JSON file
  --quick            Skip slow checks (certificate verification)
  --lang {zh,en}     Output language (zh=Chinese, en=English)
```

## Detection Modules

### 1. Proxy Detection

Checks the following:
- Proxy settings in environment variables (HTTP_PROXY, HTTPS_PROXY, etc.)
- Windows system proxy configuration (registry)
- Auto-proxy configuration URL

**Risk Level**: MEDIUM - if proxy configuration is detected

### 2. Process Detection

Scans for the following types of processes:
- Packet capture tools: Wireshark, TShark, TCPDump
- Proxy and debugging tools: Fiddler, Charles, Burp Suite, mitmproxy
- Network monitoring tools: NetworkMiner, Ettercap
- Corporate monitoring software: ActivTrak, Teramind, InterGuard

**Risk Level**: HIGH - if monitoring tool processes are detected

### 3. Network Interface Detection

Checks:
- Virtual network adapters (may indicate VPN or virtual machine)
- VPN connections (detected via common VPN ports)

**Risk Level**: MEDIUM - if virtual adapters or VPN are detected

### 4. Connection Analysis

Analyzes:
- Suspicious listening ports (proxy ports 8080, 8888, 3128, etc.)
- Established network connections
- Abnormally high number of connections to a single IP
- Network statistics

**Risk Level**: MEDIUM - if suspicious ports or connections are detected

### 5. Certificate Detection

Tests:
- Connections to well-known websites (Google, GitHub)
- Checks if certificate issuer is suspicious
- Identifies self-signed certificates (possible man-in-the-middle attack)
- Detects corporate proxy certificates (Zscaler, BlueCoat, etc.)

**Risk Level**: HIGH - if suspicious certificates or MITM signs are detected

## Sample Output

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

## Important Notes

1. **Permission Requirements**: Some detection features may require administrator privileges to obtain complete results
2. **Possible False Positives**: Some findings may be legitimate (e.g., corporate VPN, security software, etc.)
3. **Result Interpretation**: Please use your judgment to interpret the detection results based on actual circumstances
4. **Network Connection**: The certificate detection module requires an internet connection

## Disclaimer

This tool is for legitimate security checks and educational purposes only. Please ensure you have the right to run this tool on the target system. The author assumes no responsibility for misuse of the tool.

## Technology Stack

- **psutil**: System and process information
- **colorama**: Colored terminal output
- **requests**: HTTP requests (for future extensions)
- **ssl/socket**: TLS certificate detection

## Project Structure

```
check-internet-monitor/
├── main.py                    # Main entry script
├── detectors/
│   ├── __init__.py
│   ├── proxy_detector.py      # Proxy detection module
│   ├── process_detector.py    # Process detection module
│   ├── network_detector.py    # Network interface detection module
│   ├── connection_detector.py # Connection analysis module
│   └── certificate_detector.py # Certificate detection module
├── utils/
│   ├── __init__.py
│   ├── i18n.py                # Internationalization module
│   └── reporter.py            # Report generation utility
├── requirements.txt           # Dependency list
├── README.md                  # This document (English)
└── README_zh.md               # Chinese documentation
```

## Contributing

Issue reports and feature requests are welcome!

## License

MIT License

## Author

Created for educational and security research purposes.
