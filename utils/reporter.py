"""
Reporter Module
Generates formatted reports from detection results
"""
import json
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for Windows
init(autoreset=True)


class Reporter:
    def __init__(self, translator):
        self.results = []
        self.translator = translator

    def add_result(self, result):
        """Add a detection result"""
        self.results.append(result)

    def print_report(self):
        """Print colored terminal report"""
        print("\n" + "=" * 70)
        print(f"{Fore.CYAN}{Style.BRIGHT}{self.translator.t('report.title')}{Style.RESET_ALL}")
        print(f"{self.translator.t('report.generated')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70 + "\n")

        # Overall risk assessment
        overall_risk = self._calculate_overall_risk()
        risk_color = self._get_risk_color(overall_risk)
        risk_level_translated = self.translator.t(f'risk_levels.{overall_risk}')
        print(f"{Style.BRIGHT}{self.translator.t('report.overall_risk')}: {risk_color}{risk_level_translated}{Style.RESET_ALL}\n")

        # Print each detection module result
        for result in self.results:
            self._print_module_result(result)

        # Summary
        total_findings = sum(len(r['findings']) for r in self.results)
        print("\n" + "=" * 70)
        print(f"{Style.BRIGHT}{self.translator.t('report.summary')}:{Style.RESET_ALL}")
        print(f"  {self.translator.t('report.total_checks')}: {len(self.results)}")
        print(f"  {self.translator.t('report.total_findings')}: {total_findings}")
        print(f"  {self.translator.t('report.overall_risk')}: {risk_color}{risk_level_translated}{Style.RESET_ALL}")
        print("=" * 70 + "\n")

    def _print_module_result(self, result):
        """Print a single module's results"""
        risk_color = self._get_risk_color(result['risk_level'])

        # Translate module name if it's one of the standard detector names
        module_name = result['name']

        # Translate risk level
        risk_level_translated = self.translator.t(f"risk_levels.{result['risk_level']}")

        print(f"{Fore.YELLOW}{Style.BRIGHT}[{module_name}]{Style.RESET_ALL}")
        print(f"  {self.translator.t('report.risk_level')}: {risk_color}{risk_level_translated}{Style.RESET_ALL}")
        print(f"  {self.translator.t('report.findings_count')}: {len(result['findings'])}")

        if result['findings']:
            for i, finding in enumerate(result['findings'], 1):
                severity_color = self._get_severity_color(finding['severity'])
                # Translate finding type and severity
                finding_type = self.translator.t(f"findings.{finding['type']}")
                severity_translated = self.translator.t(f"severity_levels.{finding['severity']}")
                print(f"    {i}. {severity_color}[{severity_translated}]{Style.RESET_ALL} "
                      f"{finding_type}: {finding['detail']}")

        print()

    def export_json(self, filename='report.json'):
        """Export report as JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_risk': self._calculate_overall_risk(),
            'results': self.results
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"{Fore.GREEN}{self.translator.t('report.exported', filename=filename)}{Style.RESET_ALL}")

    def _calculate_overall_risk(self):
        """Calculate overall risk level from all results"""
        risk_levels = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        max_risk = max((risk_levels.get(r['risk_level'], 0) for r in self.results), default=0)

        for level, value in risk_levels.items():
            if value == max_risk:
                return level
        return 'LOW'

    def _get_risk_color(self, risk_level):
        """Get color for risk level"""
        colors = {
            'HIGH': Fore.RED + Style.BRIGHT,
            'MEDIUM': Fore.YELLOW + Style.BRIGHT,
            'LOW': Fore.GREEN + Style.BRIGHT
        }
        return colors.get(risk_level, Fore.WHITE)

    def _get_severity_color(self, severity):
        """Get color for severity"""
        colors = {
            'HIGH': Fore.RED,
            'MEDIUM': Fore.YELLOW,
            'LOW': Fore.CYAN,
            'INFO': Fore.WHITE
        }
        return colors.get(severity, Fore.WHITE)
