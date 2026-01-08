"""
Monitor Reporter Module
Specialized reporter for continuous monitoring mode
"""
from colorama import Fore, Style
from datetime import datetime
from utils.reporter import Reporter


class MonitorReporter(Reporter):
    """Reporter specialized for monitoring mode"""

    def print_monitoring_header(self, interval):
        """
        Prints the monitoring start information.

        Args:
            interval: Detection interval in seconds.
        """
        print("\n" + "=" * 70)
        print(f"{Fore.CYAN}{Style.BRIGHT}{self.translator.t('monitor.title')}{Style.RESET_ALL}")
        print(f"{self.translator.t('monitor.started')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{self.translator.t('monitor.interval')}: {interval} {self.translator.t('monitor.seconds')}")
        print(f"{self.translator.t('monitor.stop_hint')}: Ctrl+C")
        print("=" * 70)
        print(f"\n{self.translator.t('monitor.running_initial_scan')}...\n")

    def print_status_update(self, cycle, timestamp):
        """
        Prints a brief status update (when there are no changes).

        Args:
            cycle: The current cycle number.
            timestamp: The timestamp.
        """
        time_str = timestamp.strftime('%H:%M:%S')
        print(f"[{time_str}] {Fore.GREEN}✓{Style.RESET_ALL} "
              f"{self.translator.t('monitor.cycle_complete', cycle=cycle)} - "
              f"{self.translator.t('monitor.no_changes')}")

    def print_change_alert(self, changes):
        """
        Prints a change alert (highlighted).

        Args:
            changes: A dictionary of changes, including new findings and risk level changes.
        """
        timestamp = changes['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        print("\n" + "!" * 70)
        print(f"{Fore.YELLOW}{Style.BRIGHT}🔔 {self.translator.t('monitor.changes_detected')}!{Style.RESET_ALL}")
        print(f"{self.translator.t('report.generated')}: {timestamp}")
        print("!" * 70 + "\n")

        # Print new findings
        if changes.get('new_findings'):
            print(f" {Fore.RED}{Style.BRIGHT}⚠️ {self.translator.t('monitor.new_activity_detected')}{Style.RESET_ALL}")
            for item in changes['new_findings']:
                module_name = item['module']
                severity = item['severity']
                severity_color = self._get_severity_color(severity)
                severity_text = self.translator.t(f'severity_levels.{severity}')

                print(f"  {Fore.YELLOW}[{module_name}]{Style.RESET_ALL} "
                      f"{self.translator.t('report.risk_level')}: {severity_color}{severity_text}{Style.RESET_ALL}")

                for finding in item['findings']:
                    finding_type = self.translator.t(f"findings.{finding['type']}")
                    print(f"    • {finding_type}: {finding['detail']}")
                print()

        # Print removed findings
        if changes.get('removed_findings'):
            print(f" {Fore.GREEN}{Style.BRIGHT}✓ {self.translator.t('monitor.resolved_activity')}{Style.RESET_ALL}")
            for item in changes['removed_findings']:
                module_name = item['module']
                print(f"  {Fore.GREEN}[{module_name}]{Style.RESET_ALL}")

                for finding in item['findings']:
                    finding_type = self.translator.t(f"findings.{finding['type']}")
                    print(f"    • {Fore.GREEN}{finding_type}: {finding['detail']}{Style.RESET_ALL}")
                print()

        # Print risk level changes
        if changes.get('risk_changes'):
            for change in changes['risk_changes']:
                from_level = self.translator.t(f'risk_levels.{change["from"]}')
                to_level = self.translator.t(f'risk_levels.{change["to"]}')

                print(f"  {Fore.YELLOW}[{change['module']}]{Style.RESET_ALL} "
                      f"{self.translator.t('monitor.risk_changed')}: {from_level} → {to_level}")

        print("!" * 70 + "\n")
