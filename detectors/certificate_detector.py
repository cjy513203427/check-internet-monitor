"""
Certificate Detector Module
Detects suspicious SSL/TLS certificates that may indicate MITM attacks
"""
import ssl
import socket
from datetime import datetime


class CertificateDetector:
    def __init__(self, translator):
        self.findings = []
        self.risk_level = "LOW"
        self.translator = translator

    def detect(self):
        """Run certificate detection"""
        self._check_system_certificates()
        self._test_tls_interception()
        return {
            "name": self.translator.t('modules.certificate_detection'),
            "risk_level": self.risk_level,
            "findings": self.findings
        }

    def _check_system_certificates(self):
        """Check for suspicious system certificates"""
        # On Windows, checking system certificates requires pywin32 or similar
        # For now, we'll skip this and focus on TLS interception test
        pass

    def _test_tls_interception(self):
        """Test for TLS/SSL interception by connecting to known sites"""
        test_sites = [
            ('www.google.com', 443),
            ('www.github.com', 443),
        ]

        for hostname, port in test_sites:
            try:
                context = ssl.create_default_context()

                with socket.create_connection((hostname, port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()

                        # Check issuer
                        issuer = dict(x[0] for x in cert['issuer'])
                        subject = dict(x[0] for x in cert['subject'])

                        # Check for common corporate/proxy certificates
                        issuer_org = issuer.get('organizationName', '')
                        suspicious_issuers = [
                            'proxy', 'firewall', 'corporate', 'company',
                            'zscaler', 'bluecoat', 'forcepoint', 'checkpoint'
                        ]

                        if any(sus.lower() in issuer_org.lower() for sus in suspicious_issuers):
                            self.findings.append({
                                "type": "Suspicious Certificate Issuer",
                                "detail": f"{hostname}: Issued by {issuer_org} (possible MITM)",
                                "severity": "HIGH"
                            })
                            self.risk_level = "HIGH"

                        # Check if certificate is self-signed
                        if issuer == subject:
                            self.findings.append({
                                "type": "Self-Signed Certificate",
                                "detail": f"{hostname}: Certificate is self-signed (possible MITM)",
                                "severity": "HIGH"
                            })
                            self.risk_level = "HIGH"

            except ssl.SSLError as e:
                self.findings.append({
                    "type": "TLS Error",
                    "detail": f"{hostname}: SSL Error - {str(e)} (possible interception)",
                    "severity": "MEDIUM"
                })
                if self.risk_level == "LOW":
                    self.risk_level = "MEDIUM"

            except socket.timeout:
                # Timeout is not necessarily suspicious
                pass

            except Exception as e:
                # Other errors - not necessarily suspicious
                pass
