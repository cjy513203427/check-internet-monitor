English | [中文](./README_zh.md)

# Network Monitoring Detection Tool

A Python tool for detecting network monitoring on your system. This tool helps identify proxy settings, packet capture tools, suspicious network connections, and potential man-in-the-middle attacks.

## Features

- **Proxy Detection**: Check proxy configurations in system and environment variables.
- **Process Monitoring**: Identify common network packet capture and monitoring tools (e.g., Wireshark, Fiddler, Charles).
- **Network Interface Analysis**: Detect virtual network adapters and VPN connections.
- **Connection Analysis**: Check for suspicious listening ports and active connections.
- **Certificate Detection**: Test TLS/SSL connections to discover potential man-in-the-middle attacks.
- **Continuous Monitoring**: A real-time monitoring mode that periodically scans for changes and reports new and resolved threats.
- **Bilingual Support**: Supports Chinese and English output.
- **Colored Terminal Output**: Clear risk level display.
- **JSON Export**: Export detection results to JSON format (in one-time scan mode).

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
conda activate your_env_name
pip install -r requirements.txt
```

Or using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run all detections in a one-time scan:

```bash
python main.py
```

Use English output:

```bash
python main.py --lang en
```

### Continuous Monitoring Mode

Enable real-time monitoring to detect changes. The tool will scan at regular intervals and only report new or resolved findings.

```bash
# Start monitoring mode (default 30-second interval)
python main.py --monitor

# Set a custom interval (e.g., 10 seconds)
python main.py --monitor --interval 10

# Use monitoring mode with English output
python main.py --monitor --lang en

# Stop the monitor by pressing Ctrl+C
```

### Quick Mode

In a one-time scan, skip the time-consuming certificate detection:

```bash
python main.py --quick
```

### Export Results

Export one-time scan results to a JSON file:

```bash
python main.py --json report.json
```

### Command Line Options

```
usage: main.py [-h] [--json FILE] [--quick] [--lang {zh,en}] [--monitor] [--interval SECONDS]

Detect network monitoring and surveillance on your system

optional arguments:
  -h, --help            show this help message and exit
  --json FILE           Export results to JSON file
  --quick               Skip slow checks (certificate verification)
  --lang {zh,en}        Output language (zh=Chinese, en=English)
  --monitor             Enable continuous monitoring mode
  --interval SECONDS    Monitoring detection interval in seconds (default: 30)
```

## Detection Modules

The tool includes the following detection modules:

1.  **Proxy Detection**: Checks environment variables and system settings for proxies.
2.  **Process Detection**: Scans for running processes of known monitoring tools.
3.  **Network Interface Detection**: Looks for virtual adapters and signs of VPNs.
4.  **Connection Analysis**: Analyzes listening ports and established connections for suspicious patterns.
5.  **Certificate Detection**: Inspects TLS certificates of common sites for signs of interception (MITM).

## Sample Output

### One-Time Scan

The one-time scan provides a full report of all findings.

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

...
```

### Continuous Monitoring Mode

Monitoring mode starts with an initial scan and then reports only the changes.

```
======================================================================
Continuous Monitoring Mode
Started: 2024-01-15 11:00:00
Detection Interval: 30 seconds
Stop monitoring: Ctrl+C
======================================================================

Running initial scan...

[11:00:30] ✓ Cycle #1 completed - No changes detected
[11:01:00] ✓ Cycle #2 completed - No changes detected

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
🔔 System state changes detected!
Generated: 2024-01-15 11:01:30
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

 ⚠️ New monitoring activity detected:
  [Process Detection] Risk Level: HIGH
    • Suspicious Process: Fiddler (HTTP Debugger) (PID: 5678, Name: Fiddler.exe)

[11:02:00] ✓ Cycle #4 completed - No changes detected

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
🔔 System state changes detected!
Generated: 2024-01-15 11:02:30
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

 ✓ Resolved monitoring activity:
  [Process Detection]
    • Suspicious Process: Fiddler (HTTP Debugger) (PID: 5678, Name: Fiddler.exe)

```

## Important Notes

1.  **Permissions**: For best results, run with administrator/root privileges.
2.  **False Positives**: Some findings can be legitimate (e.g., corporate VPNs, antivirus software). Interpret results in context.
3.  **Network Access**: The certificate detection module requires an internet connection.

## Disclaimer

This tool is for educational and legitimate security auditing purposes only. The author is not responsible for any misuse.

## Project Structure

```
check-internet-monitor/
├── main.py                    # Main entry script
├── detectors/
│   ├── __init__.py
│   ├── proxy_detector.py
│   ├── process_detector.py
│   ├── network_detector.py
│   ├── connection_detector.py
│   └── certificate_detector.py
├── utils/
│   ├── __init__.py
│   ├── change_detector.py     # Module for comparing scan results
│   ├── i18n.py                # Internationalization module
│   ├── monitor_reporter.py    # Reporter for monitoring mode
│   ├── monitoring_service.py  # Service for continuous monitoring
│   └── reporter.py            # Base report generation utility
├── requirements.txt           # Dependency list
├── README.md                  # This document (English)
└── README_zh.md               # Chinese documentation
```

## Contributing

Feedback, issues, and pull requests are welcome.

## License

MIT License
