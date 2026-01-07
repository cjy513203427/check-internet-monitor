"""
Connection Detector Module
Analyzes network connections for suspicious patterns
"""
import psutil
from collections import defaultdict


class ConnectionDetector:
    def __init__(self, translator):
        self.findings = []
        self.risk_level = "LOW"
        self.translator = translator

        # Suspicious ports that might indicate monitoring
        self.suspicious_ports = {
            8888: 'Common Proxy Port',
            8080: 'HTTP Proxy',
            3128: 'Squid Proxy',
            1080: 'SOCKS Proxy',
            9050: 'Tor SOCKS',
            8118: 'Privoxy',
            9150: 'Tor Browser',
        }

    def detect(self):
        """Run connection analysis"""
        self._check_listening_ports()
        self._check_established_connections()
        self._analyze_connection_patterns()
        return {
            "name": self.translator.t('modules.connection_analysis'),
            "risk_level": self.risk_level,
            "findings": self.findings
        }

    def _check_listening_ports(self):
        """Check for suspicious listening ports"""
        try:
            connections = psutil.net_connections(kind='inet')

            listening_ports = []
            for conn in connections:
                if conn.status == 'LISTEN' and hasattr(conn, 'laddr') and conn.laddr:
                    port = conn.laddr.port
                    listening_ports.append(port)

                    if port in self.suspicious_ports:
                        self.findings.append({
                            "type": "Suspicious Listening Port",
                            "detail": f"Port {port} ({self.suspicious_ports[port]}) - PID: {conn.pid}",
                            "severity": "MEDIUM"
                        })
                        if self.risk_level == "LOW":
                            self.risk_level = "MEDIUM"

        except (psutil.AccessDenied, PermissionError):
            self.findings.append({
                "type": "Permission",
                "detail": "Insufficient permissions to check all listening ports (try running as administrator)",
                "severity": "INFO"
            })
        except Exception as e:
            self.findings.append({
                "type": "Error",
                "detail": f"Failed to check listening ports: {str(e)}",
                "severity": "INFO"
            })

    def _check_established_connections(self):
        """Check established connections for suspicious patterns"""
        try:
            connections = psutil.net_connections(kind='inet')

            # Count connections by remote address
            remote_addrs = defaultdict(int)
            suspicious_connections = []

            for conn in connections:
                if conn.status == 'ESTABLISHED' and hasattr(conn, 'raddr') and conn.raddr:
                    remote_ip = conn.raddr.ip
                    remote_port = conn.raddr.port

                    remote_addrs[remote_ip] += 1

                    # Check for suspicious remote ports
                    if remote_port in self.suspicious_ports:
                        suspicious_connections.append({
                            'ip': remote_ip,
                            'port': remote_port,
                            'description': self.suspicious_ports[remote_port]
                        })

            # Report if too many connections to single IP
            for ip, count in remote_addrs.items():
                if count > 10:  # Arbitrary threshold
                    self.findings.append({
                        "type": "Multiple Connections",
                        "detail": f"{count} connections to {ip}",
                        "severity": "LOW"
                    })

            # Report suspicious connections
            for conn in suspicious_connections:
                self.findings.append({
                    "type": "Suspicious Remote Connection",
                    "detail": f"Connected to {conn['ip']}:{conn['port']} ({conn['description']})",
                    "severity": "MEDIUM"
                })
                if self.risk_level == "LOW":
                    self.risk_level = "MEDIUM"

        except (psutil.AccessDenied, PermissionError):
            pass
        except Exception as e:
            self.findings.append({
                "type": "Error",
                "detail": f"Failed to check connections: {str(e)}",
                "severity": "INFO"
            })

    def _analyze_connection_patterns(self):
        """Analyze overall connection patterns"""
        try:
            # Get network I/O statistics
            net_io = psutil.net_io_counters()

            # Just informational
            self.findings.append({
                "type": "Network Statistics",
                "detail": f"Sent: {self._format_bytes(net_io.bytes_sent)}, Received: {self._format_bytes(net_io.bytes_recv)}",
                "severity": "INFO"
            })

        except Exception as e:
            pass

    def _format_bytes(self, bytes_count):
        """Format bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.2f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.2f} PB"
