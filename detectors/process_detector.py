"""
Process Detector Module
Detects common network monitoring and packet capture tools
"""
import psutil


class ProcessDetector:
    def __init__(self, translator):
        self.findings = []
        self.risk_level = "LOW"
        self.translator = translator

        # Common monitoring/sniffing tools
        self.suspicious_processes = {
            # Packet capture tools
            'wireshark.exe': 'Wireshark (Packet Analyzer)',
            'wireshark': 'Wireshark (Packet Analyzer)',
            'tshark.exe': 'TShark (Wireshark CLI)',
            'tshark': 'TShark (Wireshark CLI)',
            'tcpdump': 'TCPDump (Packet Analyzer)',
            'windump.exe': 'WinDump (Packet Analyzer)',

            # Proxy and debugging tools
            'fiddler.exe': 'Fiddler (HTTP Debugger)',
            'charles.exe': 'Charles Proxy',
            'burpsuite': 'Burp Suite (Security Testing)',
            'mitmproxy': 'mitmproxy (MITM Proxy)',
            'proxifier.exe': 'Proxifier',

            # Network monitoring
            'networkminer.exe': 'NetworkMiner',
            'ettercap': 'Ettercap (Network Sniffer)',
            'cain.exe': 'Cain & Abel',

            # Corporate monitoring
            'bvckup2.exe': 'Backup Software (may monitor files)',
            'activtrack': 'ActivTrak (Employee Monitoring)',
            'teramind': 'Teramind (Employee Monitoring)',
            'interguard': 'InterGuard (Monitoring)',
        }

    def detect(self):
        """Run process detection"""
        self._check_running_processes()
        return {
            "name": self.translator.t('modules.process_detection'),
            "risk_level": self.risk_level,
            "findings": self.findings
        }

    def _check_running_processes(self):
        """Check for suspicious running processes"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()

                    for suspicious_name, description in self.suspicious_processes.items():
                        if suspicious_name.lower() in proc_name:
                            self.findings.append({
                                "type": "Suspicious Process",
                                "detail": f"{description} (PID: {proc.info['pid']}, Name: {proc.info['name']})",
                                "severity": "HIGH"
                            })
                            self.risk_level = "HIGH"

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        except Exception as e:
            self.findings.append({
                "type": "Error",
                "detail": f"Failed to enumerate processes: {str(e)}",
                "severity": "INFO"
            })
