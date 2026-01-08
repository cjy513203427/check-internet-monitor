"""
Internationalization (i18n) module for bilingual support.
Provides translation management for Chinese and English languages.
"""


class TranslationManager:
    """Manages translations for multiple languages."""

    def __init__(self, language='zh'):
        """
        Initialize the translation manager.

        Args:
            language (str): Default language ('zh' for Chinese, 'en' for English)
        """
        self.language = language
        self.translations = TRANSLATIONS

    def set_language(self, language):
        """
        Set the current language.

        Args:
            language (str): Language code ('zh' or 'en')
        """
        if language in self.translations:
            self.language = language
        else:
            # Fallback to English if invalid language
            self.language = 'en'

    def t(self, key, **kwargs):
        """
        Translate a message key with optional variable substitution.

        Args:
            key (str): Translation key in dot notation (e.g., 'cli.description')
            **kwargs: Variables for template substitution

        Returns:
            str: Translated message with variables substituted
        """
        # Navigate through nested dictionary using dot notation
        keys = key.split('.')
        value = self.translations.get(self.language, {})

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, key)  # Fallback to key if not found
            else:
                return key

        # If value is still a dict, something went wrong, return the key
        if isinstance(value, dict):
            return key

        # Substitute variables if provided
        if kwargs:
            try:
                return value.format(**kwargs)
            except (KeyError, ValueError):
                # If formatting fails, return the unformatted string
                return value

        return value


# Translation dictionaries for all supported languages
TRANSLATIONS = {
    'zh': {
        # CLI Arguments
        'cli': {
            'description': '检测系统上的网络监控和监视',
            'epilog': '''示例:
  python main.py                     # 运行所有检查
  python main.py --json report.json  # 导出结果到JSON
  python main.py --quick             # 跳过缓慢的检查
  python main.py --lang en           # 使用英文输出
  python main.py --monitor           # 启用持续监控模式''',
            'help_json': '将结果导出到JSON文件',
            'help_quick': '跳过缓慢的检查(证书验证)',
            'help_lang': '输出语言 (zh=中文, en=英文)',
            'help_monitor': '启用持续监控模式',
            'help_interval': '监控检测间隔(秒，默认30秒)',
        },

        # Progress Messages
        'progress': {
            'starting': '开始网络监控检测...',
            'please_wait': '这可能需要一些时间...\n',
            'checking_proxy': '检查代理设置...',
            'scanning_processes': '扫描监控进程...',
            'analyzing_network': '分析网络接口...',
            'examining_connections': '检查网络连接...',
            'testing_certificates': '测试TLS/SSL证书...',
            'skipping_certificates': '跳过证书检查(快速模式)\n',
        },

        # Module Names
        'modules': {
            'proxy_detection': '代理检测',
            'process_detection': '进程检测',
            'network_detection': '网络接口检测',
            'connection_analysis': '连接分析',
            'certificate_detection': '证书检测',
        },

        # Finding Types
        'findings': {
            'Environment Proxy': '环境变量代理',
            'Windows System Proxy': 'Windows系统代理',
            'Windows Auto-Config Proxy': 'Windows自动配置代理',
            'Suspicious Process': '可疑进程',
            'Virtual Network Adapter': '虚拟网络适配器',
            'VPN Connection': 'VPN连接',
            'Suspicious Listening Port': '可疑监听端口',
            'Permission': '权限',
            'Multiple Connections': '多个连接',
            'Suspicious Remote Connection': '可疑远程连接',
            'Network Statistics': '网络统计',
            'Suspicious Certificate Issuer': '可疑证书颁发者',
            'Self-Signed Certificate': '自签名证书',
            'TLS Error': 'TLS错误',
            'Error': '错误',
        },

        # Detail Templates
        'templates': {
            'env_proxy': '{var}={value}',
            'proxy_server': '代理服务器: {server}',
            'auto_config_url': '自动配置URL: {url}',
            'process_found': '{desc} (PID: {pid}, 名称: {name})',
            'virtual_adapter': '接口: {interface} (可能表示VPN或虚拟机)',
            'vpn_detected': '检测到 {vpn_type} 连接',
            'listening_port': '端口 {port} ({desc}) - PID: {pid}',
            'permission_denied': '权限不足,无法检查所有监听端口(请尝试以管理员身份运行)',
            'multiple_conns': '{count} 个连接到 {ip}',
            'remote_conn': '连接到 {ip}:{port} ({desc})',
            'net_stats': '发送: {sent}, 接收: {recv}',
            'cert_issuer': '{hostname}: 由 {org} 颁发 (可能存在MITM)',
            'self_signed': '{hostname}: 证书为自签名 (可能存在MITM)',
            'tls_error': '{hostname}: SSL错误 - {error} (可能被拦截)',
            'failed_to_run': '运行检测器失败: {error}',
            'failed_check': '检查失败: {error}',
        },

        # Report Labels
        'report': {
            'title': '网络监控检测报告',
            'generated': '生成时间',
            'overall_risk': '总体风险级别',
            'risk_level': '风险级别',
            'findings_count': '发现',
            'summary': '摘要',
            'total_checks': '总检查数',
            'total_findings': '总发现数',
            'exported': '报告已导出到: {filename}',
        },

        # Risk Levels
        'risk_levels': {
            'HIGH': '高',
            'MEDIUM': '中',
            'LOW': '低',
        },

        # Severity Levels
        'severity_levels': {
            'HIGH': '高',
            'MEDIUM': '中',
            'LOW': '低',
            'INFO': '信息',
        },

        # Final Messages
        'messages': {
            'note': '注意: 此工具提供潜在监控的指示器。',
            'note2': '某些发现可能是合法的(企业VPN、安全软件等)',
            'note3': '请根据实际情况判断结果。\n',
            'cancelled': '\n\n操作已被用户取消。',
            'fatal_error': '\n致命错误: {error}',
            'detector_error': '运行 {detector} 时出错: {error}',
        },

        # Monitoring Mode
        'monitor': {
            'title': '持续监控模式',
            'started': '启动时间',
            'interval': '检测间隔',
            'seconds': '秒',
            'stop_hint': '停止监控',
            'running_initial_scan': '正在执行初始扫描',
            'cycle_complete': '周期 #{cycle} 完成',
            'no_changes': '未发现变化',
            'changes_detected': '检测到系统状态变化',
            'new_activity_detected': '发现新的监控活动:',
            'resolved_activity': '已解决的监控活动:',
            'risk_changed': '风险级别变化',
            'stopping': '正在停止监控...',
        },
    },

    'en': {
        # CLI Arguments
        'cli': {
            'description': 'Detect network monitoring and surveillance on your system',
            'epilog': '''Examples:
  python main.py                     # Run all checks
  python main.py --json report.json  # Export results to JSON
  python main.py --quick             # Skip slow checks
  python main.py --lang zh           # Use Chinese output
  python main.py --monitor           # Enable continuous monitoring''',
            'help_json': 'Export results to JSON file',
            'help_quick': 'Skip slow checks (certificate verification)',
            'help_lang': 'Output language (zh=Chinese, en=English)',
            'help_monitor': 'Enable continuous monitoring mode',
            'help_interval': 'Monitoring detection interval in seconds (default: 30)',
        },

        # Progress Messages
        'progress': {
            'starting': 'Starting network monitoring detection...',
            'please_wait': 'This may take a few moments...\n',
            'checking_proxy': 'Checking proxy settings...',
            'scanning_processes': 'Scanning for monitoring processes...',
            'analyzing_network': 'Analyzing network interfaces...',
            'examining_connections': 'Examining network connections...',
            'testing_certificates': 'Testing TLS/SSL certificates...',
            'skipping_certificates': 'Skipping certificate checks (--quick mode)\n',
        },

        # Module Names
        'modules': {
            'proxy_detection': 'Proxy Detection',
            'process_detection': 'Process Detection',
            'network_detection': 'Network Interface Detection',
            'connection_analysis': 'Connection Analysis',
            'certificate_detection': 'Certificate Detection',
        },

        # Finding Types
        'findings': {
            'Environment Proxy': 'Environment Proxy',
            'Windows System Proxy': 'Windows System Proxy',
            'Windows Auto-Config Proxy': 'Windows Auto-Config Proxy',
            'Suspicious Process': 'Suspicious Process',
            'Virtual Network Adapter': 'Virtual Network Adapter',
            'VPN Connection': 'VPN Connection',
            'Suspicious Listening Port': 'Suspicious Listening Port',
            'Permission': 'Permission',
            'Multiple Connections': 'Multiple Connections',
            'Suspicious Remote Connection': 'Suspicious Remote Connection',
            'Network Statistics': 'Network Statistics',
            'Suspicious Certificate Issuer': 'Suspicious Certificate Issuer',
            'Self-Signed Certificate': 'Self-Signed Certificate',
            'TLS Error': 'TLS Error',
            'Error': 'Error',
        },

        # Detail Templates
        'templates': {
            'env_proxy': '{var}={value}',
            'proxy_server': 'Proxy Server: {server}',
            'auto_config_url': 'Auto-config URL: {url}',
            'process_found': '{desc} (PID: {pid}, Name: {name})',
            'virtual_adapter': 'Interface: {interface} (may indicate VPN or VM)',
            'vpn_detected': 'Detected {vpn_type} connection',
            'listening_port': 'Port {port} ({desc}) - PID: {pid}',
            'permission_denied': 'Insufficient permissions to check all listening ports (try running as administrator)',
            'multiple_conns': '{count} connections to {ip}',
            'remote_conn': 'Connected to {ip}:{port} ({desc})',
            'net_stats': 'Sent: {sent}, Received: {recv}',
            'cert_issuer': '{hostname}: Issued by {org} (possible MITM)',
            'self_signed': '{hostname}: Certificate is self-signed (possible MITM)',
            'tls_error': '{hostname}: SSL Error - {error} (possible interception)',
            'failed_to_run': 'Failed to run detector: {error}',
            'failed_check': 'Failed to check: {error}',
        },

        # Report Labels
        'report': {
            'title': 'Network Monitoring Detection Report',
            'generated': 'Generated',
            'overall_risk': 'Overall Risk Level',
            'risk_level': 'Risk Level',
            'findings_count': 'Findings',
            'summary': 'Summary',
            'total_checks': 'Total Checks',
            'total_findings': 'Total Findings',
            'exported': 'Report exported to: {filename}',
        },

        # Risk Levels
        'risk_levels': {
            'HIGH': 'HIGH',
            'MEDIUM': 'MEDIUM',
            'LOW': 'LOW',
        },

        # Severity Levels
        'severity_levels': {
            'HIGH': 'HIGH',
            'MEDIUM': 'MEDIUM',
            'LOW': 'LOW',
            'INFO': 'INFO',
        },

        # Final Messages
        'messages': {
            'note': 'Note: This tool provides indicators of potential monitoring.',
            'note2': 'Some findings may be legitimate (corporate VPN, security software, etc.)',
            'note3': 'Use your judgment to interpret the results.\n',
            'cancelled': '\n\nOperation cancelled by user.',
            'fatal_error': '\nFatal error: {error}',
            'detector_error': 'Error running {detector}: {error}',
        },

        # Monitoring Mode
        'monitor': {
            'title': 'Continuous Monitoring Mode',
            'started': 'Started',
            'interval': 'Detection Interval',
            'seconds': 'seconds',
            'stop_hint': 'Stop monitoring',
            'running_initial_scan': 'Running initial scan',
            'cycle_complete': 'Cycle #{cycle} completed',
            'no_changes': 'No changes detected',
            'changes_detected': 'System state changes detected',
            'new_activity_detected': 'New monitoring activity detected:',
            'resolved_activity': 'Resolved monitoring activity:',
            'risk_changed': 'Risk level changed',
            'stopping': 'Stopping monitoring...',
        },
    },
}


# Create a global translator instance with Chinese as default
translator = TranslationManager(language='zh')
