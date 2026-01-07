"""
Network Detector Module
Detects network interface configurations that may indicate monitoring
"""
import psutil
import platform


class NetworkDetector:
    def __init__(self, translator):
        self.findings = []
        self.risk_level = "LOW"
        self.translator = translator

    def detect(self):
        """Run network interface detection"""
        self._check_network_interfaces()
        self._check_vpn_connections()
        return {
            "name": self.translator.t('modules.network_detection'),
            "risk_level": self.risk_level,
            "findings": self.findings
        }

    def _check_network_interfaces(self):
        """Check network interfaces for suspicious configurations"""
        try:
            interfaces = psutil.net_if_stats()

            for interface_name, stats in interfaces.items():
                # Check for promiscuous mode (not easily detectable on Windows without admin)
                # On Windows, this requires admin privileges or special tools

                # Check for virtual network adapters (VPN, VM, etc.)
                if self._is_virtual_adapter(interface_name):
                    self.findings.append({
                        "type": "Virtual Network Adapter",
                        "detail": f"Interface: {interface_name} (may indicate VPN or VM)",
                        "severity": "MEDIUM"
                    })
                    if self.risk_level == "LOW":
                        self.risk_level = "MEDIUM"

        except Exception as e:
            self.findings.append({
                "type": "Error",
                "detail": f"Failed to check network interfaces: {str(e)}",
                "severity": "INFO"
            })

    def _is_virtual_adapter(self, interface_name):
        """Check if interface is a virtual adapter"""
        virtual_keywords = [
            'vmware', 'virtualbox', 'vbox', 'virtual', 'tap', 'tun',
            'vpn', 'openvpn', 'wireguard', 'nordvpn', 'expressvpn',
            'tunnelbear', 'protonvpn', 'mullvad', 'hyper-v'
        ]

        interface_lower = interface_name.lower()
        return any(keyword in interface_lower for keyword in virtual_keywords)

    def _check_vpn_connections(self):
        """Check for active VPN connections"""
        try:
            # Check network connections for VPN-related ports
            connections = psutil.net_connections()

            vpn_ports = {
                1194: 'OpenVPN',
                1723: 'PPTP VPN',
                500: 'IKEv2/IPSec',
                4500: 'IPSec NAT-T',
                51820: 'WireGuard'
            }

            vpn_found = set()
            for conn in connections:
                if hasattr(conn, 'laddr') and conn.laddr:
                    port = conn.laddr.port
                    if port in vpn_ports:
                        vpn_found.add(vpn_ports[port])

            for vpn_type in vpn_found:
                self.findings.append({
                    "type": "VPN Connection",
                    "detail": f"Detected {vpn_type} connection",
                    "severity": "MEDIUM"
                })
                if self.risk_level == "LOW":
                    self.risk_level = "MEDIUM"

        except (psutil.AccessDenied, PermissionError):
            # Need admin rights to see all connections
            pass
        except Exception as e:
            self.findings.append({
                "type": "Error",
                "detail": f"Failed to check VPN connections: {str(e)}",
                "severity": "INFO"
            })
