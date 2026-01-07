"""
Proxy Detector Module
Detects system and environment proxy settings
"""
import os
import platform


class ProxyDetector:
    def __init__(self, translator):
        self.findings = []
        self.risk_level = "LOW"
        self.translator = translator

    def detect(self):
        """Run all proxy detection checks"""
        self._check_env_proxies()
        self._check_system_proxies()
        return {
            "name": self.translator.t('modules.proxy_detection'),
            "risk_level": self.risk_level,
            "findings": self.findings
        }

    def _check_env_proxies(self):
        """Check environment variables for proxy settings"""
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'FTP_PROXY', 'ALL_PROXY',
                     'http_proxy', 'https_proxy', 'ftp_proxy', 'all_proxy']

        for var in proxy_vars:
            value = os.environ.get(var)
            if value:
                self.findings.append({
                    "type": "Environment Proxy",
                    "detail": f"{var}={value}",
                    "severity": "MEDIUM"
                })
                self.risk_level = "MEDIUM"

    def _check_system_proxies(self):
        """Check system-level proxy settings"""
        if platform.system() == "Windows":
            self._check_windows_proxy()

    def _check_windows_proxy(self):
        """Check Windows registry for proxy settings"""
        try:
            import winreg

            # Check Internet Settings
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)

                # Check if proxy is enabled
                try:
                    proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
                    if proxy_enable:
                        try:
                            proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
                            self.findings.append({
                                "type": "Windows System Proxy",
                                "detail": f"Proxy Server: {proxy_server}",
                                "severity": "MEDIUM"
                            })
                            self.risk_level = "MEDIUM"
                        except FileNotFoundError:
                            pass
                except FileNotFoundError:
                    pass

                # Check auto-config URL
                try:
                    auto_config_url, _ = winreg.QueryValueEx(key, "AutoConfigURL")
                    if auto_config_url:
                        self.findings.append({
                            "type": "Windows Auto-Config Proxy",
                            "detail": f"Auto-config URL: {auto_config_url}",
                            "severity": "MEDIUM"
                        })
                        self.risk_level = "MEDIUM"
                except FileNotFoundError:
                    pass

                winreg.CloseKey(key)
            except FileNotFoundError:
                pass

        except ImportError:
            # winreg not available on non-Windows platforms
            pass
